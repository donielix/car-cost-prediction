from functools import wraps


def delete_fitted_attributes_if_error(func):
    @wraps(func)
    def wrapper(self, X, y):
        try:
            return func(self, X, y)
        except Exception:
            if hasattr(self, "X_"):
                del self.X_
            if hasattr(self, "y_"):
                del self.y_
            raise

    return wrapper
