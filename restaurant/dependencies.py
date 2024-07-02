from core.dependencies import ContentTypeChecker


class RestaurantContentTypeChecker(ContentTypeChecker):
    def __init__(self) -> None:
        content_types = ['image/png', 'image/jpeg', 'image/jpg']
        super(RestaurantContentTypeChecker, self).__init__(content_types)
