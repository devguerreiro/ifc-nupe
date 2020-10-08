from django.test import TestCase
from model_bakery import baker

from nupe.core.models import AccountAttendance, Attendance


class AttendanceTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(Attendance, "_safedelete_policy"), True)
        self.assertIs(hasattr(Attendance, "attendance_reason"), True)
        self.assertIs(hasattr(Attendance, "attendance_severity"), True)
        self.assertIs(hasattr(Attendance, "attendants"), True)
        self.assertIs(hasattr(Attendance, "student"), True)
        self.assertIs(hasattr(Attendance, "status"), True)
        self.assertIs(hasattr(Attendance, "opened_at"), True)
        self.assertIs(hasattr(Attendance, "closed_at"), True)

    def test_return_str(self):
        attendance = baker.prepare(Attendance)

        str_expected = (
            f"{attendance.student} - {attendance.attendance_severity} - {attendance.attendance_reason.description}"
        )
        self.assertEqual(str(attendance), str_expected)


class AccountAttendanceTestCase(TestCase):
    def test_has_all_attributes(self):
        self.assertIs(hasattr(AccountAttendance, "_safedelete_policy"), True)
        self.assertIs(hasattr(AccountAttendance, "annotation"), True)
        self.assertIs(hasattr(AccountAttendance, "attendance"), True)
        self.assertIs(hasattr(AccountAttendance, "account"), True)
        self.assertIs(hasattr(AccountAttendance, "attendance_at"), True)
        self.assertIs(hasattr(AccountAttendance, "updated_at"), True)

    def test_return_str(self):
        account_attendance = baker.prepare(AccountAttendance)

        str_expected = f"{account_attendance.account.full_name} - {account_attendance.annotation}"
        self.assertEqual(str(account_attendance), str_expected)
