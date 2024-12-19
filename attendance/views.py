import datetime
from rest_framework import viewsets
from users.models import ClassSchedule
from .models import Attendance
from .serializers import AttendanceSerializer

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        teacher = self.request.user
        # O'qituvchiga biriktirilgan guruhlar va dars jadvali orqali sanalarni olish
        schedules = ClassSchedule.objects.filter(teacher=teacher)
        attendance_dates = []
        for schedule in schedules:
            # O'qituvchining dars sanalarini avtomatik aniqlash
            start_date = schedule.time_start
            end_date = schedule.time_end
            # Avtomatik ravishda dars sanalarini generatsiya qilish
            attendance_dates.append({'schedule': schedule, 'dates': get_dates_for_schedule(start_date, end_date)})
        return attendance_dates


def get_dates_for_schedule(start_date, end_date):
    current_date = datetime.date.today()
    dates = []

    # Sanalar oralig'ida hafta kunlari bo'yicha sanalarni topish
    while current_date <= end_date:
        if current_date.weekday() in (0, 2, 4):  # Misol uchun, darslar dushanba, chorshanba, juma kunlari bo'ladi
            dates.append(current_date)
        current_date += datetime.timedelta(days=1)

    return dates