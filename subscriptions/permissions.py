
from rest_framework.exceptions import PermissionDenied

def require_hd_export(user):
    subscription = getattr(user, "subscription", None)

    if not subscription or not subscription.plan.allow_hd_export:
        raise PermissionDenied(
            detail="HD export is not available on your current plan."
        )

def should_apply_watermark(user) -> bool:
    subscription = getattr(user, "subscription", None)

    # Default: apply watermark
    if not subscription:
        return True

    return not subscription.plan.remove_watermark
