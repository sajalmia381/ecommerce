from .signal import object_viewed_signal


class ObjectsViewedMixin(object):

    def get_context_data(self, *args, **kwargs):
        context = super(ObjectsViewedMixin, self).get_context_data(*args, **kwargs)
        request = self.request
        instance = context.get('object')
        if instance:
            object_viewed_signal.send(instance.__class__, instance=instance, request=request)
        return context
