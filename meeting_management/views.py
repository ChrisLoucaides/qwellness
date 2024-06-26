from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from user_management.models import Student, Advisor
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

        return JsonResponse({'success': True, 'meeting_id': meeting.id}, status=201)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required()
def create_meeting_advisor(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        advisor_id = data.get('id')
        student_username = data.get('student')
        meeting_date = data.get('date')
        meeting_time = data.get('time')

        if not advisor_id or not student_username or not meeting_date or not meeting_time:
            return JsonResponse({'error': 'Advisor ID, Student Username, date, and time are required'}, status=400)

        try:
            advisor = Advisor.objects.get(id=advisor_id)
        except Advisor.DoesNotExist:
            return JsonResponse({'error': 'Advisor not found'}, status=404)

        student = Student.objects.get(username=student_username)

        if not student:
            return JsonResponse({'error': 'Advisor does not have a student assigned'}, status=400)

        if not student.advisor:
            return JsonResponse({'error': 'Student is not assigned to any advisor'}, status=400)

        meeting = Meeting.objects.create(
            student=student,
            advisor=advisor,
            date=meeting_date,
            time=meeting_time
        )

        return JsonResponse({'success': True, 'meeting_id': meeting.id}, status=201)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
def get_student_meetings(request):
    if request.method == 'GET':
        student_id = request.GET.get('id')
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)

        if not student_id:
            return JsonResponse({'error': 'Student ID is required'}, status=400)

        try:
            student_meetings = Meeting.objects.filter(student_id=student.id)
            meetings_data = [{'id': meeting.id, 'date': meeting.date, 'time': meeting.time} for meeting in
                             student_meetings]
            return JsonResponse({'meetings': meetings_data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
def get_advisor_meetings(request):
    if request.method == 'GET':
        advisor_id = request.GET.get('id')

        try:
            advisor = Advisor.objects.get(id=advisor_id)
        except Advisor.DoesNotExist:
            return JsonResponse({'error': 'Advisor not found'}, status=404)

        if not advisor_id:
            return JsonResponse({'error': 'Advisor ID is required'}, status=400)

        try:
            advisor_meetings = Meeting.objects.filter(advisor_id=advisor.id)
            meetings_data = [{'id': meeting.id, 'student': meeting.student.username, 'date': meeting.date, 'time': meeting.time}
                             for meeting in advisor_meetings]
            return JsonResponse({'meetings': meetings_data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required()
def delete_meeting(request):
    if request.method == 'DELETE':
        data = json.loads(request.body.decode('utf-8'))

        meeting_id = data.get('id')

        if not meeting_id:
            return JsonResponse({'error': 'Meeting ID is required'}, status=400)

        try:
            meeting = Meeting.objects.get(id=meeting_id)
            meeting.delete()
        except Meeting.DoesNotExist:
            return JsonResponse({'error': 'Meeting not found'}, status=404)

        return JsonResponse({'success': True, 'meeting_id': meeting.id}, status=200)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
