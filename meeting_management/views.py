from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from user_management.models import Student
from meeting_management.models import Meeting


@login_required
def create_meeting_student(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        student_id = data.get('id')
        meeting_date = data.get('date')
        meeting_time = data.get('time')

        if not student_id or not meeting_date or not meeting_time:
            return JsonResponse({'error': 'Student ID, date, and time are required'}, status=400)

        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)

        advisor = student.advisor

        if not advisor:
            return JsonResponse({'error': 'Student does not have an advisor assigned'}, status=400)

        meeting = Meeting.objects.create(
            student=student,
            advisor=advisor,
            date=meeting_date,
            time=meeting_time
        )

        if not student.advisor_meeting_ids:
            student.advisor_meeting_ids = []
        student.advisor_meeting_ids.append(meeting.id)
        student.save()

        return JsonResponse({'success': True, 'meeting_id': meeting.id}, status=201)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
