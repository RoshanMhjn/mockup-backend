
from rest_framework.exceptions import PermissionDenied

def require_hd_export(user):
    subscription = getattr(user, "subscription", None)

    if not subscription or not subscription.plan.allow_hd_export:
        raise PermissionDenied(
            detail="HD export is not available on your current plan."
        )

def should_apply_watermark(user) -> bool:
    subscription = getattr(user, "subscription", None)

    if not subscription:
        return True

    return not subscription.plan.remove_watermark

def require_premium_templates(user):
    subscription = getattr(user, "subscription", None)
    
    if not subscription or not subscription.plan.allow_premium_templates:
        raise PermissionDenied(
            detail="Premium templates are not available on your current plan."
        )
