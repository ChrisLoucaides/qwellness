from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from task_management.models import Task
from user_management.models import Student


@login_required
def create_task(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        name = request.POST.get('name')
        due_date = request.POST.get('due_date')
        description = request.POST.get('description')

        try:
            student = Student.objects.get(username=username)
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)

        task = Task.objects.create(
            name=name,
            due_date=due_date,
            description=description,
            student=student
        )

        if not student.task_ids:
            student.task_ids = []
        student.task_ids.append(task.id)
        student.save()

        return JsonResponse({'success': True, 'task_id': task.id}, status='201')
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
def get_student_tasks(request):
    if request.method == 'GET':
        username = request.GET.get('username')

        try:
            student = Student.objects.get(username=username)
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)

        tasks = Task.objects.filter(student=student)

        serialized_tasks = [
            {
                'id': task.id,
                'name': task.name,
                'due_date': task.due_date,
                'description': task.description,
                'completed': task.completed
            }
            for task in tasks
        ]

        return JsonResponse({'tasks': serialized_tasks})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
