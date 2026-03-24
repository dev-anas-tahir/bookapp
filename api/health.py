from litestar import get
from litestar.openapi.datastructures import ResponseSpec
from litestar.openapi.spec.example import Example


@get(
    "/health",
    sync_to_thread=False,
    responses={
        200: ResponseSpec(
            data_container=dict[str, str],
            description="OK",
            generate_examples=False,
            examples=[
                Example(
                    summary="Healthy",
                    value={"status": "healthy"},
                )
            ],
        )
    },
)
def health_check() -> dict[str, str]:
    """Health check endpoint for load balancers."""
    return {"status": "healthy"}
