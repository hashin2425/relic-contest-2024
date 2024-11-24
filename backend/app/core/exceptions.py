""" カスタム例外を定義するモジュール """

from fastapi import HTTPException, status


class AuthenticationError(HTTPException):
    """認証エラー"""

    def __init__(self, detail: str = "認証に失敗しました"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class PermissionDeniedError(HTTPException):
    """権限エラー"""

    def __init__(self, detail: str = "権限がありません"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


class NotFoundError(HTTPException):
    """リソースが見つからないエラー"""

    def __init__(self, detail: str = "リソースが見つかりません"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )


class ValidationError(HTTPException):
    """バリデーションエラー"""

    def __init__(self, detail: str = "入力データが無効です"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
        )


class ServiceUnavailableError(HTTPException):
    """サービス利用不可エラー"""

    def __init__(self, detail: str = "サービスが利用できません"):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail,
        )
