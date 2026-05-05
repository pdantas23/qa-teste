from typing import Any
from faker import Faker

_faker = Faker("pt_BR")


class FabricaPet:
    @staticmethod
    def pet_valido(status: str = "available") -> dict[str, Any]:
        return {
            "id": _faker.random_int(min=1, max=999_999),
            "name": _faker.first_name(),
            "status": status,
            "photoUrls": [_faker.image_url()],
            "category": {"id": _faker.random_int(min=1, max=10), "name": _faker.word()},
            "tags": [{"id": _faker.random_int(min=1, max=100), "name": _faker.word()}],
        }

    @staticmethod
    def pet_atualizado(id_pet: int, nome: str | None = None, status: str = "sold") -> dict[str, Any]:
        return {
            "id": id_pet,
            "name": nome or _faker.first_name(),
            "status": status,
            "photoUrls": [_faker.image_url()],
        }


class FabricaPedido:
    @staticmethod
    def pedido_valido(id_pet: int) -> dict[str, Any]:
        return {
            "id": _faker.random_int(min=1, max=999_999),
            "petId": id_pet,
            "quantity": _faker.random_int(min=1, max=5),
            "shipDate": "2025-12-01T00:00:00.000Z",
            "status": "placed",
            "complete": False,
        }


class FabricaUsuario:
    @staticmethod
    def usuario_valido() -> dict[str, Any]:
        nome_usuario = _faker.user_name() + str(_faker.random_int(min=100, max=999))
        return {
            "id": _faker.random_int(min=1, max=999_999),
            "username": nome_usuario,
            "firstName": _faker.first_name(),
            "lastName": _faker.last_name(),
            "email": _faker.email(),
            "password": _faker.password(length=12),
            "phone": _faker.phone_number(),
            "userStatus": 1,
        }
