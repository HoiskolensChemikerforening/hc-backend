from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import PostForm
from .models import Puns_Submission


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
            "Vitsen ble mottatt, tusen takk!",
            extra_tags="Du dro en vits",
        )
        return redirect(reverse("puns:index"))
    context = {"form": form}

    return render(request, "/post_f.html", context)


@permission_required("puns.change_submission")
def submissions_overview(request):
    all_submissions = (
        Puns_Submission.objects.all()
        .order_by("-date")
        .prefetch_related("author__profile")
    )

    paginator = Paginator(all_submissions, 20)
    page_number = int(request.GET.get("page", 1))

    try:
        puns_submission_page = paginator.page(page_number)
    except PageNotAnInteger:
        puns_submission_page = paginator.page(1)
    except EmptyPage:
        puns_submission_page = paginator.page(paginator.num_pages)

    useful_page_range = list(puns_submission_page.paginator.page_range)
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

    puns_submission_page.paginator.first_page = paginator.page(
        useful_page_range[0]
    ).number
    puns_submission_page.paginator.last_page = paginator.page(
        useful_page_range[-1]
    ).number

    context = {
        "puns_submission_page": puns_submission_page,
        "limit_useful_page_range": limit_useful_page_range,
    }

    return render(request, "/list_sub.html", context=context)


@permission_required("puns.change_submission")
def toggle_used(request):
    if request.method == "POST":
        submission = Puns_Submission.objects.get(id=request.POST["id"])
        submission.accepted = not submission.accepted
        submission.save()
        return JsonResponse({"used": submission.accepted})
    else:
        return redirect("puns:list")
