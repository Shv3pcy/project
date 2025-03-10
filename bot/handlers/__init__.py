from aiogram import Router
from .start import router as start_router
from .bmi import router as bmi_router
from .number_systems import router as number_systems_router
from .crypto import router as crypto_router
from .system import router as system_router

# Main router that includes all other routers
router = Router()

# Include all feature routers
router.include_router(start_router)
router.include_router(bmi_router)
router.include_router(number_systems_router)
router.include_router(crypto_router)
router.include_router(system_router)