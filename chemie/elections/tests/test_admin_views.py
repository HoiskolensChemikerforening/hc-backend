import pytest
from django.shortcuts import reverse
from ..models import Election, Candidate, Ticket
from chemie.customprofile.models import Profile
from django.core.exceptions import ObjectDoesNotExist


@pytest.mark.django_db
def test_basic_user_admin_page_no_open_election(client, create_user):
    user = create_user

    client.login(username=user.username, password="defaultpassword")

    # Check that basic user is redirected to login page
    request = client.get(reverse("elections:admin_start_election"))
    assert request.status_code == 302
    assert reverse("login") in request.url

    # Check that basic user is redirected to login page
    request = client.get(reverse("elections:admin_end_election"))
    assert request.status_code == 302
    assert reverse("login") in request.url

    # Check that basic user is redirected to login page
    request = client.get(reverse("elections:admin_register_positions"))
    assert request.status_code == 302
    assert reverse("login") in request.url

    # Check that basic user is redirected to login page
    request = client.get(reverse("elections:admin_results", kwargs={"pk": 1}))
    assert request.status_code == 302
    assert reverse("login") in request.url


@pytest.mark.django_db
def test_admin_user_admin_page_no_open_election(client, create_admin_user):
    user = create_admin_user
    client.login(username=user.username, password="defaultpassword")

    # Check that admin user can access start election
    request = client.get(reverse("elections:admin_start_election"))
    assert request.status_code == 200
    assert (
        "Trykk på Start for å sette igang et valg"
        in request.content.decode("utf-8")
    )

    # Check that admin user is redirected to start election
    # when election does not exist
    request = client.get(reverse("elections:admin_end_election"))
    assert request.status_code == 302
    assert request.url == reverse("elections:admin_start_election")

    # Check that admin user is redirected to start election
    # when election does not exist
    request = client.get(reverse("elections:admin_register_positions"))
    assert request.status_code == 302
    assert request.url == reverse("elections:admin_start_election")

    # Check that admin user is redirected to start election
    # when election does not exist
    request = client.get(
        reverse("elections:admin_register_candidates", kwargs={"pk": 1})
    )
    assert request.status_code == 302
    assert request.url == reverse("elections:admin_start_election")

    # Check that admin user is redirected to start election
    # when election does not exist
    request = client.get(reverse("elections:admin_results", kwargs={"pk": 1}))
    assert request.status_code == 302
    assert request.url == reverse("elections:admin_start_election")

    # Check that user is redirected to start election
    # if he tries to start voting for position
    request = client.get(
        reverse("elections:admin_start_voting", kwargs={"pk": 1})
    )
    assert request.status_code == 302
    assert request.url == reverse("elections:admin_start_election")


@pytest.mark.django_db
def test_admin_open_election(client, create_admin_user):
    user = create_admin_user
    client.login(username=user.username, password="defaultpassword")
    assert Election.objects.all().count() == 0
    client.post(reverse("elections:admin_start_election"))
    assert Election.objects.all().count() == 1
    election = Election.objects.all().first()
    assert election.positions.all().count() == 0
    assert election.is_open
    assert not election.current_position_is_active()
    assert election.current_position is None

    request = client.get(reverse("elections:admin_end_election"))
    assert request.status_code == 302
    assert request.url == reverse(
        "elections:previous_election", kwargs={"pk": election.pk}
    )


@pytest.mark.django_db
def test_admin_add_positions(client, create_admin_user, create_open_election):
    admin = create_admin_user
    client.login(username=admin.username, password="defaultpassword")
    election = create_open_election
    position_name = "position_name"
    position_spots = 2
    client.post(
        reverse("elections:admin_register_positions"),
        {"position_name": position_name, "spots": position_spots},
    )

    assert election.positions.all().count() == 1
    assert election.positions.all().first().position_name == position_name
    assert election.positions.all().first().spots == position_spots
    assert election.positions.all().first().get_total_votes() == 0
    assert election.positions.all().first().candidates.all().count() == 0
    assert not election.positions.all().first().is_done


@pytest.mark.django_db
def test_delete_position(
    client, create_admin_user, create_election_with_positions
):
    admin = create_admin_user
    client.login(username=admin.username, password="defaultpassword")
    election, positions = create_election_with_positions
    election.is_open = True
    [election.positions.add(position) for position in positions]

    # create_election_with_positions will allways create five positions
    assert election.positions.all().count() == 5

    position = positions[0]
    assert position in election.positions.all()
    client.post(
        reverse("elections:admin_delete_position"), {"Delete": position.id}
    )
    assert election.positions.all().count() == 4
    with pytest.raises(ObjectDoesNotExist) as e_info:
        position.refresh_from_db()


@pytest.mark.django_db
def test_add_candidates(
    client, create_admin_user, create_election_with_positions, create_user
):
    admin = create_admin_user
    client.login(username=admin.username, password="defaultpassword")
    election, postitions = create_election_with_positions
    election.is_open = True
    position = postitions[0]
    election.add_position(position.position_name, position.spots)
    election.save()
    user = create_user

    client.post(
        reverse(
            "elections:admin_register_candidates", kwargs={"pk": position.id}
        ),
        {"user": user.id, "addCandidate": "Legg til kandidat"},
    )

    position.refresh_from_db()
    assert position.candidates.all().count() == 1
    candidate = Candidate.objects.get(user=user)
    assert candidate is not None
    assert candidate.votes == 0
    assert candidate in position.candidates.all()


@pytest.mark.django_db
def test_add_pre_votes_to_candidate(
    client,
    create_admin_user,
    create_open_election_with_position_and_candidates,
):
    admin = create_admin_user
    client.login(username=admin.username, password="defaultpassword")
    election = create_open_election_with_position_and_candidates
    position = election.positions.all().first()
    # Votes before trying to add pre_votes
    old_votes = position.get_total_votes()
    cands = position.candidates.all()
    number_of_candidates = cands.count()
    cands = list(cands)  # Do not remove this bad boy!
    candidate = cands[0]

    pre_votes = 5
    post_data = {
        "candidate_forms-TOTAL_FORMS": number_of_candidates,
        "candidate_forms-INITIAL_FORMS": number_of_candidates,
        "candidate_forms-MIN_NUM_FORMS": "0",
        "candidate_forms-MAX_NUM_FORMS": "1000",
        "candidate_forms-0-pre_votes": pre_votes,
        "candidate_forms-0-id": cands[0].pk,
        "candidate_forms-1-pre_votes": 0,
        "candidate_forms-1-id": cands[1].pk,
        "candidate_forms-2-pre_votes": 0,
        "candidate_forms-2-id": cands[2].pk,
        "candidate_forms-3-pre_votes": 0,
        "candidate_forms-3-id": cands[3].pk,
        "total_voters-number_of_prevote_tickets": pre_votes,
    }
    client.post(
        reverse(
            "elections:admin_register_prevotes", kwargs={"pk": position.id}
        ),
        data=post_data,
        follow=True,
    )
    candidate.refresh_from_db()
    position.refresh_from_db()

    assert candidate.pre_votes == pre_votes
    assert position.get_total_votes() == (old_votes + pre_votes)

    # Testing that the votes of other candidates has not changed.
    assert (
        position.candidates.filter(pre_votes=0).count()
        == number_of_candidates - 1
    )


@pytest.mark.django_db
def test_delete_candidate_from_position(
    client,
    create_admin_user,
    create_open_election_with_position_and_candidates,
):
    admin = create_admin_user
    client.login(username=admin.username, password="defaultpassword")
    election = create_open_election_with_position_and_candidates
    position = election.positions.all().first()
    number_of_candidates = position.candidates.all().count()
    candidate = position.candidates.all().first()
    candidate_user = candidate.user

    client.post(
        reverse(
            "elections:admin_delete_candidate", kwargs={"pk": position.id}
        ),
        {"Delete": candidate.user.username},
    )
    position.refresh_from_db()
    assert position.candidates.all().count() == number_of_candidates - 1
    with pytest.raises(ObjectDoesNotExist) as e_info:
        Candidate.objects.get(user=candidate_user)


@pytest.mark.django_db
def test_start_voting_for_current_position(
    create_admin_user,
    client,
    create_open_election_with_position_and_candidates,
):
    admin = create_admin_user
    client.login(username=admin.username, password="defaultpassword")
    election = create_open_election_with_position_and_candidates
    position = election.positions.all().first()
    assert not election.current_position_is_active()
    client.post(
        reverse(
            "elections:admin_register_candidates", kwargs={"pk": position.id}
        ),
        {"startVoting": position.id},
    )
    position.refresh_from_db()
    assert position.get_total_votes() == 0
    for profile in Profile.objects.all():
        assert not profile.voted


@pytest.mark.django_db
def test_start_voting_for_current_position_with_pre_votes(
    create_admin_user,
    client,
    create_open_election_with_position_and_candidates,
):
    admin = create_admin_user
    client.login(username=admin.username, password="defaultpassword")
    election = create_open_election_with_position_and_candidates
    position = election.positions.all().first()
    number_of_candidates = position.candidates.all().count()

    for candidate in position.candidates.all():
        candidate.pre_votes = 1
        candidate.save()
    client.post(
        reverse("elections:admin_start_voting", kwargs={"pk": position.id}),
    )
    position.refresh_from_db()
    assert position.get_total_votes() == number_of_candidates
    for profile in Profile.objects.all():
        assert not profile.voted


@pytest.mark.django_db
def test_admin_urls_when_voting_is_active(
    create_admin_user,
    client,
    create_open_election_with_position_and_candidates,
):
    admin = create_admin_user
    client.login(username=admin.username, password="defaultpassword")
    election = create_open_election_with_position_and_candidates
    position = election.positions.all().first()
    election.current_position = position
    election.save()

    # Check that user is redirected to register position
    # if position is open for voting
    request = client.get(
        reverse("elections:admin_start_election"), follow=True
    )
    assert (
        reverse("elections:admin_register_positions"),
        302,
    ) == request.redirect_chain[0]
    assert position.position_name in request.content.decode("utf-8")

    # Check that user is redirected to register position
    # when no current position is open
    request = client.get(
        reverse("elections:admin_start_voting", kwargs={"pk": position.id}),
        follow=True,
    )
    assert (
        reverse(
            "elections:admin_register_candidates", kwargs={"pk": position.id}
        ),
        302,
    ) == request.redirect_chain[0]
    for pos in election.positions.all():
        assert pos.position_name in request.content.decode("utf-8")

    # Open current position for voting
    election.current_position.is_active = True
    election.current_position.save()

    request = client.get(
        reverse(
            "elections:admin_register_candidates", kwargs={"pk": position.id}
        )
    )
    assert request.status_code == 302
    assert (
        reverse("elections:admin_voting_active", kwargs={"pk": position.id})
        == request.url
    )

    request = client.get(
        reverse("elections:admin_results", kwargs={"pk": position.id})
    )
    assert request.status_code == 302
    assert (
        reverse("elections:admin_voting_active", kwargs={"pk": position.id})
        == request.url
    )

    request = client.get(reverse("elections:admin_start_election"))
    assert request.status_code == 302
    assert (
        reverse("elections:admin_voting_active", kwargs={"pk": position.id})
        == request.url
    )

    request = client.get(reverse("elections:admin_register_positions"))
    assert request.status_code == 302

    # Check that when user tries to access open voting for position
    # and voting is already open, he is redirected
    request = client.get(
        reverse("elections:admin_start_voting", kwargs={"pk": position.id}),
        follow=True,
    )
    assert request.redirect_chain[0] == (
        reverse("elections:admin_voting_active", kwargs={"pk": position.id}),
        302,
    )
    assert "personer har stemt" in request.content.decode("utf-8")

    # Now end voting for position by pressing "end" button
    # and see that voting for position closes
    request = client.post(
        reverse("elections:admin_voting_active", kwargs={"pk": position.id}),
        follow=True,
    )
    assert (
        reverse("elections:admin_results", kwargs={"pk": position.id}),
        302,
    ) == request.redirect_chain[0]
    for cand in position.candidates.all():
        assert cand.user.get_full_name() in request.content.decode("utf-8")

    request = client.get(reverse("elections:admin_end_election"))
    assert request.status_code == 302
    assert request.url == reverse(
        "elections:previous_election", kwargs={"pk": election.pk}
    )


@pytest.mark.django_db
def test_admin_view_results(
    create_admin_user,
    client,
    create_open_election_with_position_and_candidates,
):
    admin = create_admin_user
    client.login(username=admin.username, password="defaultpassword")
    election = create_open_election_with_position_and_candidates
    position = election.positions.all().first()
    candidates = position.candidates.all()
    winners = candidates[: position.spots]
    for candidate in winners:
        position.vote([candidate], admin)
        admin.profile.voted = False
        admin.profile.save()
    election.start_current_position_voting(position.id)
    election.end_current_position_voting()

    # Refresh election and position and check results
    election.refresh_from_db()
    position.refresh_from_db()
    request = client.get(
        reverse("elections:admin_results", kwargs={"pk": position.id})
    )
    total_votes = position.get_total_votes()
    assert request.status_code == 200
    assert total_votes == position.spots
    assert position.get_total_candidate_ticket_votes() == total_votes
    assert position.get_total_candidate_prevotes() == 0
    assert position.get_blank_votes() == 0
