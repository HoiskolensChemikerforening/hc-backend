from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser

from .forms import PostForm
from .models import Submission
from .serializers import SubmissionSerializer


@login_required
def post_votes(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()
        messages.add_message(
            request,
            messages.SUCCESS,
            "Sladderet ble mottatt, tusen takk!",
            extra_tags="Du sladret",
        )
        return redirect(reverse("shitbox:index"))
    context = {"form": form}

    return render(request, "shitbox/post_form.html", context)


@permission_required("shitbox.change_submission")
def submissions_overview(request):
    all_submissions = (
        Submission.objects.all()
        .order_by("-date")
        .prefetch_related("author__profile")
    )

    paginator = Paginator(all_submissions, 20)
    page_number = int(request.GET.get("page", 1))

    try:
        submission_page = paginator.page(page_number)
    except PageNotAnInteger:
        submission_page = paginator.page(1)
    except EmptyPage:
        submission_page = paginator.page(paginator.num_pages)

    useful_page_range = list(submission_page.paginator.page_range)
    limit_useful_page_range = []

    if page_number - 2 in paginator.page_range:
        limit_useful_page_range.append(page_number - 2)
    if page_number - 1 in paginator.page_range:
        limit_useful_page_range.append(page_number - 1)
    if page_number in paginator.page_range:
        limit_useful_page_range.append(page_number)
    if page_number + 1 in paginator.page_range:
        limit_useful_page_range.append(page_number + 1)
    if page_number + 2 in paginator.page_range:
        limit_useful_page_range.append(page_number + 2)

    submission_page.paginator.first_page = paginator.page(
        useful_page_range[0]
    ).number
    submission_page.paginator.last_page = paginator.page(
        useful_page_range[-1]
    ).number

    context = {
        "submission_page": submission_page,
        "limit_useful_page_range": limit_useful_page_range,
    }

    return render(request, "shitbox/list_submissions.html", context=context)


@permission_required("shitbox.change_submission")
def toggle_used(request):
    if request.method == "POST":
        submission = Submission.objects.get(id=request.POST["id"])
        submission.used = not submission.used
        submission.save()
        return JsonResponse({"used": submission.used})
    else:
        return redirect("shitbox:list")


class SubmissionListView(generics.ListCreateAPIView):
    parser_class = [MultiPartParser, FormParser]
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer


class SubmissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
