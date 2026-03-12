from django.shortcuts import render, redirect
from .models import WorkLog
from .forms import WorkLogForm
from django.contrib.auth.models import User
from django.db.models import Count
from reportlab.pdfgen import canvas
from django.http import HttpResponse
import openpyxl
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db.models import Q
from django.core.paginator import Paginator


# Create your views here.
@login_required
def index(request):
    total_logs = WorkLog.objects.count()
    completed = WorkLog.objects.filter(status="Completed").count()
    pending = WorkLog.objects.filter(status="Pending").count()
    progress = WorkLog.objects.filter(status="In Progress").count()

    context = {
        "total_logs": total_logs,
        "completed": completed,
        "pending": pending,
        "progress": progress,
        "title": "dashboard"
    }
    
    return render(request, 'logs/index.html', context)

@login_required
def addLog(request):
    
    if request.method == "POST":
        form = WorkLogForm(request.POST)

        if form.is_valid():
            log = form.save(commit=False)
            log.employee = request.user  # automatically assign the logged-in user
            log.save()

            return redirect('logs:viewLogs')

    else:
        form = WorkLogForm()

    return render(request, 'logs/addLog.html', {"title": "addLog" , "form": form})

@login_required
def viewLogs(request):
    
    logs = WorkLog.objects.all().order_by('-date')
    
    search = request.GET.get('search')
    status = request.GET.get('status')

    # Search filter
    if search:
        logs = logs.filter(
            Q(ticket_id__icontains=search) |
            Q(task__icontains=search) |
            Q(location__icontains=search) |
            Q(problem__icontains=search)
        )

    # Status filter
    if status:
        logs = logs.filter(status=status)


    
    return render(request, 'logs/viewLog.html', {"title": "viewLogs" , "logs": logs})


@login_required
def reports(request):

    logs = WorkLog.objects.all()

    # Get filters from GET parameters
    start_date = request.GET.get("start_date")  # YYYY-MM-DD format
    end_date = request.GET.get("end_date")      # YYYY-MM-DD format
    status = request.GET.get("status")
    employee = request.GET.get("employee")
    sort = request.GET.get("sort")

    # 1️⃣ Filter by ticket date (optional)
    if start_date:
        logs = logs.filter(date__gte=start_date)

    if end_date:
        logs = logs.filter(date__lte=end_date)

    # 2️⃣ Filter by status
    if status:
        logs = logs.filter(status=status)

    # 3️⃣ Filter by employee
    if employee:
        logs = logs.filter(employee_id=employee)

    # 4️⃣ Sorting
    if sort == "date":
        logs = logs.order_by("-date")
    elif sort == "status":
        logs = logs.order_by("status")
    elif sort == "employee":
        logs = logs.order_by("employee__username")

    # 5️⃣ Statistics for cards
    total_logs = logs.count()
    completed = logs.filter(status="Completed").count()
    pending = logs.filter(status="Pending").count()
    progress = logs.filter(status="In Progress").count()

    # 6️⃣ Employee stats for chart
    employee_stats = logs.values('employee__username').annotate(total=Count('id'))

    # 7️⃣ Get all employees for filter dropdown
    employees = User.objects.all()

    context = {
        "logs": logs,
        "employees": employees,
        "total_logs": total_logs,
        "completed": completed,
        "pending": pending,
        "progress": progress,
        "employee_stats": employee_stats
    }

    return render(request, "logs/report.html", context)


def export_excel(request):

    logs = WorkLog.objects.all()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Work Logs"

    ws.append(["Ticket", "Date", "Employee", "Task", "Status"])

    for log in logs:
        ws.append([
            log.ticket_id,
            str(log.date),
            str(log.employee),
            log.task,
            log.status
        ])

    response = HttpResponse(
        content_type="application/ms-excel"
    )

    response['Content-Disposition'] = 'attachment; filename="work_logs.xlsx"'

    wb.save(response)

    return response



def export_pdf(request):

    logs = WorkLog.objects.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="work_logs.pdf"'

    p = canvas.Canvas(response)

    y = 800

    p.drawString(200, 820, "Work Log Report")

    for log in logs:

        text = f"{log.ticket_id}  {log.date}  {log.employee}  {log.status}"

        p.drawString(50, y, text)

        y -= 20

    p.showPage()
    p.save()

    return response