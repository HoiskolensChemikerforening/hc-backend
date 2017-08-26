from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import PostForm
from .models import Submission

@login_required
def post_votes(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()
        messages.add_message(request, messages.SUCCESS,
                             'Sladderet ble mottatt, tusen takk!',
                             extra_tags='Du sladret')
        return redirect(reverse('shitbox:index'))
    context = {
        "form": form,
    }

    return render(request, "shitbox/post_form.html", context)


@permission_required('shitbox.change_submission')
def submissions_overview(request, page=1):
    page = int(page)
    all_submissions = Submission.objects.all().order_by('-date').prefetch_related('author__profile')
    paginator = Paginator(all_submissions, 1)

    try:
        submissions = paginator.page(page)
    except PageNotAnInteger:
        submissions = paginator.page(1)
    except EmptyPage:
        submissions = paginator.page(paginator.num_pages)

    useful_page_range = list(submissions.paginator.page_range)
    limit_useful_page_range = []
    
    if page-2 in paginator.page_range:
        limit_useful_page_range.append(page-2)
    if page-1 in paginator.page_range:
        limit_useful_page_range.append(page-1)
    if page in paginator.page_range:
        limit_useful_page_range.append(page)
    if page+1 in paginator.page_range:
        limit_useful_page_range.append(page+1)
    if page+2 in paginator.page_range:
        limit_useful_page_range.append(page+2)

    len_range = len(list(submissions.paginator.page_range))
    submissions.paginator.first_page = paginator.page(useful_page_range[0]).number
    submissions.paginator.last_page = paginator.page(useful_page_range[-1]).number

    context = {
        'submissions': submissions,
        'len_range': len_range,
        'limit_useful_page_range': limit_useful_page_range,
        'page': page,
    }

    return render(request, 'shitbox/list_submissions.html', context=context)
