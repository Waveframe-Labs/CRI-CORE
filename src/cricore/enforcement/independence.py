from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Mapping, Optional, Tuple

from ..errors import FailureClass
from ..results.stage import StageResult


Identity = Tuple[str, str]  # (id, type)


def _extract_identity(actor: Mapping[str, Any]) -> Optional[Identity]:
    i = actor.get("id")
    t = actor.get("type")
    if not isinstance(i, str) or not i.strip():
        return None
    if not isinstance(t, str) or not t.strip():
        return None
    return (i, t)


def _extract_role(actor: Mapping[str, Any]) -> Optional[str]:
    r = actor.get("role")
    if not isinstance(r, str) or not r.strip():
        return None
    return r


def run_independence_stage(
    *,
    proposal: Mapping[str, Any],
    compiled_contract: Mapping[str, Any],
    run_context: Optional[Mapping[str, Any]] = None,
) -> StageResult:
    """
    Structural independence and non-circular validation enforcement.

    Domain-agnostic structural model:

      run_context.identities.actors:        list[{id, type, role}]
      run_context.identities.required_roles: list[str] (optional; if present must be satisfied)
      run_context.identities.conflict_flags: map[str -> bool] (optional)

    Enforcement (structural only):
      - identities section must exist (stage fails if missing/invalid)
      - if required_roles is not present: stage passes (structural minimum)
      - if required_roles is present: all required roles must be satisfied by exactly one actor
      - actors satisfying required roles must be distinct identities (no single identity can satisfy 2 required roles)
      - if conflict_flags marks a required-role actor_id as true: stage fails
    """

    messages: List[str] = []
    failure_classes: List[FailureClass] = []

    identities: Optional[Mapping[str, Any]] = None
    if not run_context or not isinstance(run_context, Mapping):
        messages.append("run_context is missing or not a mapping")
        failure_classes.append(FailureClass.INDEPENDENCE_CHECK_FAILED)
    else:
        identities_obj = run_context.get("identities")
        if not isinstance(identities_obj, Mapping):
            messages.append("identities section missing from run_context")
            failure_classes.append(FailureClass.INDEPENDENCE_CHECK_FAILED)
        else:
            identities = identities_obj

    # If identities is missing/invalid, fail fast (cannot evaluate).
    if identities is None:
        return StageResult(
            stage_id="independence",
            passed=False,
            failure_classes=failure_classes,
            messages=messages,
            checked_at_utc=datetime.now(timezone.utc).isoformat(),
            engine_version=None,
        )

    # Extract optional required_roles.
    required_roles_raw = identities.get("required_roles", None)
    if required_roles_raw is None:
        # Structural minimum: identities present, but no required role surface declared.
        return StageResult(
            stage_id="independence",
            passed=not failure_classes,
            failure_classes=failure_classes,
            messages=messages,
            checked_at_utc=datetime.now(timezone.utc).isoformat(),
            engine_version=None,
        )

    # If required_roles is present, it must be a non-empty list of strings.
    if not isinstance(required_roles_raw, list):
        messages.append("identities.required_roles declared but not a list")
        failure_classes.append(FailureClass.INDEPENDENCE_CHECK_FAILED)
        required_roles: List[str] = []
    else:
        required_roles = [r for r in required_roles_raw if isinstance(r, str) and r.strip()]

    if not required_roles:
        messages.append("identities.required_roles declared but empty/invalid (cannot be satisfied)")
        failure_classes.append(FailureClass.INDEPENDENCE_CHECK_FAILED)

    # Extract actors list (required when required_roles declared).
    actors_raw = identities.get("actors")
    if not isinstance(actors_raw, list):
        messages.append("identities.actors missing or not a list (required when required_roles declared)")
        failure_classes.append(FailureClass.INDEPENDENCE_CHECK_FAILED)
        actors: List[Mapping[str, Any]] = []
    else:
        actors = [a for a in actors_raw if isinstance(a, Mapping)]

    if not actors:
        messages.append("identities.actors contains no valid actor entries")
        failure_classes.append(FailureClass.INDEPENDENCE_CHECK_FAILED)

    # Extract conflict flags (optional).
    conflict_flags_raw = identities.get("conflict_flags", {})
    conflict_flags: Dict[str, bool] = {}
    if conflict_flags_raw is None:
        conflict_flags_raw = {}
    if isinstance(conflict_flags_raw, Mapping):
        for k, v in conflict_flags_raw.items():
            if isinstance(k, str) and isinstance(v, bool):
                conflict_flags[k] = v
    else:
        messages.append("identities.conflict_flags present but not a mapping; ignoring")

    # Build role -> list[Identity] for actors, and track identities used across roles.
    role_to_identities: Dict[str, List[Identity]] = {}
    identity_to_roles: Dict[Identity, List[str]] = {}

    for idx, actor in enumerate(actors):
        ident = _extract_identity(actor)
        role = _extract_role(actor)

        if ident is None or role is None:
            messages.append(f"actors[{idx}] missing or invalid id/type/role")
            continue

        role_to_identities.setdefault(role, []).append(ident)
        identity_to_roles.setdefault(ident, []).append(role)

    # Enforce: each required role must be satisfied by exactly one actor identity.
    satisfied_identities: Dict[str, Identity] = {}
    for role in required_roles:
        candidates = role_to_identities.get(role, [])
        if len(candidates) == 0:
            messages.append(f"required role not satisfied: {role}")
            failure_classes.append(FailureClass.INDEPENDENCE_CHECK_FAILED)
            continue
        if len(candidates) > 1:
            messages.append(f"required role has multiple candidates (must be exactly one): {role}")
            failure_classes.append(FailureClass.INDEPENDENCE_CHECK_FAILED)
            continue
        satisfied_identities[role] = candidates[0]

    # Enforce distinct identities across all satisfied required roles.
    seen: Dict[Identity, str] = {}
    for role, ident in satisfied_identities.items():
        if ident in seen:
            other_role = seen[ident]
            messages.append(
                f"identity reused across required roles (violates independence): {ident[0]} ({ident[1]}) "
                f"used for roles '{other_role}' and '{role}'"
            )
            failure_classes.append(FailureClass.INDEPENDENCE_CHECK_FAILED)
        else:
            seen[ident] = role

    # Enforce conflict flags for required-role actors (if present and true => fail).
    for role, ident in satisfied_identities.items():
        actor_id = ident[0]
        if conflict_flags.get(actor_id) is True:
            messages.append(f"conflict-of-interest flag set for required role '{role}' (actor_id={actor_id})")
            failure_classes.append(FailureClass.INDEPENDENCE_CHECK_FAILED)

    # Enforce non-circular participation: if a single identity appears in multiple actor entries
    # AND participates in more than one required role, it is already caught above.
    # Here we additionally flag identities that appear with multiple roles where at least one is required.
    for ident, roles in identity_to_roles.items():
        distinct_roles = sorted(set([r for r in roles if isinstance(r, str) and r.strip()]))
        if len(distinct_roles) > 1:
            if any(r in required_roles for r in distinct_roles):
                messages.append(
                    f"identity appears with multiple roles including a required role (potential circularity): "
                    f"{ident[0]} ({ident[1]}) roles={distinct_roles}"
                )
                failure_classes.append(FailureClass.INDEPENDENCE_CHECK_FAILED)

    passed = not failure_classes

    return StageResult(
        stage_id="independence",
        passed=passed,
        failure_classes=failure_classes,
        messages=messages,
        checked_at_utc=datetime.now(timezone.utc).isoformat(),
        engine_version=None,
    )
