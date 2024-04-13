import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from task_management.models import Task
from user_management.models import Student


@login_required()
def create_task(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        username = data.get('username')
        name = data.get('name')
        due_date = data.get('due_date')
        description = data.get('description')

        if not username:
            return JsonResponse({'error': 'Username is required'}, status=400)

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

        return JsonResponse({'success': True, 'task_id': task.id}, status=201)
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


@login_required()
def update_task(request):
    if request.method == 'PUT':
        data = json.loads(request.body.decode('utf-8'))

        task_id = data.get('id')
        name = data.get('name')
        due_date = data.get('due_date')
        description = data.get('description')

        if not task_id:
            return JsonResponse({'error': 'Task ID is required'}, status=400)

        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found'}, status=404)

        if name:
            task.name = name
        if due_date:
            task.due_date = due_date
        if description:
            task.description = description

        task.save()

        return JsonResponse({'success': True, 'task_id': task.id})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required()
def delete_task(request):
    pass
