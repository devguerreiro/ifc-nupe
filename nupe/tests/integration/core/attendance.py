from django.urls import reverse
from model_bakery import baker
from rest_framework.test import APITestCase

from nupe.core.models import Attendance
from nupe.tests.integration.account.setup.account import create_account_with_permissions_and_do_authentication

from rest_framework.status import (  # HTTP_204_NO_CONTENT,; HTTP_400_BAD_REQUEST,; HTTP_403_FORBIDDEN,
    HTTP_200_OK,
    HTTP_201_CREATED,
)


class AttendanceAPITestCase(APITestCase):
    def test_list_with_permission(self):
        # cria um atendimento no banco para retornar no list
        baker.make(Attendance)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_attendance"])
        url = reverse("attendance-list")

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os dados não mascarados do banco de dados
        self.assertEqual(response.data.get("count"), Attendance.objects.count())

        data = response.data.get("results")[0]

        # campos que devem ser retornados
        self.assertIsNotNone(data.get("id"))
        self.assertIsNotNone(data.get("attendants"))
        self.assertIsNotNone(data.get("student"))
        self.assertIsNotNone(data.get("status"))

        # campos que não devem ser retornados
        self.assertIsNone(data.get("_safedelete_policy"))
        self.assertIsNone(data.get("attendance_reason"))
        self.assertIsNone(data.get("attendance_severity"))
        self.assertIsNone(data.get("opened_at"))
        self.assertIsNone(data.get("closed_at"))

    def test_retrieve_with_permission(self):
        # cria um atendimento no banco para detalhar suas informações
        attendance = baker.make(Attendance)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_attendance"])
        url = reverse("attendance-detail", args=[attendance.id])

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar as informações do atendimento fornecido
        self.assertEqual(response.data.get("attendance_reason"), str(attendance.attendance_reason))

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("attendance_severity"))
        self.assertIsNotNone(response.data.get("attendants"))
        self.assertIsNotNone(response.data.get("student"))
        self.assertIsNotNone(response.data.get("status"))
        self.assertIsNotNone(response.data.get("opened_at"))
        self.assertIsNot(response.data.get("closed_at", False), False)

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))

    def test_create_with_permission(self):
        # atendimento com informações válidas para conseguir criar
        attendance_reason = baker.make("core.AttendanceReason")
        student = baker.make("core.Student")

        attendance = {
            "attendance_reason": attendance_reason.id,
            "attendance_severity": "L",
            "student": student.id,
        }

        client = create_account_with_permissions_and_do_authentication(permissions=["core.add_attendance"])
        url = reverse("attendance-list")

        response = client.post(path=url, data=attendance)

        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # deve ser criado no banco de dados
        attendance = Attendance.objects.get(pk=response.data.get("id"))
        self.assertEqual(attendance.attendance_reason, attendance_reason)
        self.assertEqual(Attendance.objects.count(), 1)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("attendance_reason"))
        self.assertIsNotNone(response.data.get("attendance_severity"))
        self.assertIsNotNone(response.data.get("student"))
        self.assertIsNotNone(response.data.get("status"))
        self.assertIsNot(response.data.get("attendants", False), False)

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("opened_at"))
        self.assertIsNone(response.data.get("closed_at"))


# def test_partial_update_with_permission(self):
#     # cria uma função/cargo para conseguir atualiza-lo
#     function = baker.make(Function)

#     client = create_account_with_permissions_and_do_authentication(permissions=["core.change_function"])
#     url = reverse("function-detail", args=[function.id])

#     # somente um campo e com informação válida para conseguir atualizar
#     new_name = "nameupdated"
#     function_data = {"name": new_name}

#     response = client.patch(path=url, data=function_data)

#     self.assertEqual(response.status_code, HTTP_200_OK)

#     # deve ser atualizado no banco
#     self.assertEqual(Function.objects.get(pk=function.id).name, new_name)

#     # campos que devem ser retornados
#     self.assertIsNotNone(response.data.get("id"))
#     self.assertIsNotNone(response.data.get("name"))
#     self.assertIsNot(response.data.get("description", False), False)

#     # campos que não devem ser retornados
#     self.assertIsNone(response.data.get("_safedelete_policy"))
#     self.assertIsNone(response.data.get("workers"))

# def test_destroy_with_permission(self):
#     # cria uma função/cargo no banco para conseguir mascara-lo
#     function = baker.make(Function)

#     client = create_account_with_permissions_and_do_authentication(permissions=["core.delete_function"])
#     url = reverse("function-detail", args=[function.id])

#     response = client.delete(path=url)

#     self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

#     # deve ser mascarado
#     self.assertEqual(Function.objects.count(), 1)

#     # mas deve ser mantido no banco de dados
#     # uma função/cargo é criada em 'create_account_with_permissions_and_do_authentication', por isso deve conter 2
#     self.assertEqual(Function.all_objects.count(), 2)

# def test_list_without_permission(self):
#     client = create_account_with_permissions_and_do_authentication()

#     url = reverse("function-list")
#     response = client.get(path=url)

#     # não deve ter permissão para acessar
#     self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

# def test_retrieve_without_permission(self):
#     client = create_account_with_permissions_and_do_authentication()

#     url = reverse("function-detail", args=[99])
#     response = client.get(path=url)

#     # não deve ter permissão para acessar
#     self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

# def test_create_without_permission(self):
#     client = create_account_with_permissions_and_do_authentication()

#     url = reverse("function-list")
#     response = client.post(path=url, data={})

#     # não deve ter permissão para acessar
#     self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

# def test_partial_update_without_permission(self):
#     client = create_account_with_permissions_and_do_authentication()

#     url = reverse("function-detail", args=[99])
#     response = client.patch(path=url)

#     # não deve ter permissão para acessar
#     self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

# def test_destroy_without_permission(self):
#     client = create_account_with_permissions_and_do_authentication()

#     url = reverse("function-detail", args=[99])
#     response = client.delete(path=url)

#     # não deve ter permissão para acessar
#     self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)