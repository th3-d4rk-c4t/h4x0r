from bs4 import BeautifulSoup
from django.urls import reverse


def test_ovh_homepage(client):
    response = client.get("/")
    assert b"I am already an OVHcloud customer" in response.content
    assert b"I'm new to OVHcloud" in response.content


def test_dashboard_homepage(client):
    response = client.get(reverse("dashboard"))
    assert b"Welcome back, dear members of our community!" in response.content


def test_dashboard_get_login(client):
    response = client.get(reverse("login"))
    soup = BeautifulSoup(response.content.decode(), features="html.parser")
    text = soup.find("form").find_next("legend").get_text()
    assert text == "H4x0rs Only - Step 1/2"


def test_dashboard_post_login_errors(db, client):
    response = client.post(reverse("login"), data={"foo": "bar"})
    soup = BeautifulSoup(response.content.decode(), features="html.parser")
    text = soup.find(id="error_1_id_username").find_next("strong").get_text()
    assert text == "This field is required."

    response = client.post(
        reverse("login"), data={"username": "doesnotexist"}, follow=True
    )
    soup = BeautifulSoup(response.content.decode(), features="html.parser")
    text = soup.find_all("div", {"class": "alert-danger"})[0].find_next("p").get_text()
    assert response.status_code == 200
    assert response.redirect_chain == [("/d4shb04rd-f0r-1337/login/", 302)]
    assert text == "Member does not exist"


def test_dashboard_post_login_success(db, client):
    response = client.post(reverse("login"), data={"username": "john"}, follow=True)
    assert response.status_code == 200
    assert response.redirect_chain == [("/d4shb04rd-f0r-1337/question/", 302)]

    soup = BeautifulSoup(response.content.decode(), features="html.parser")
    title = soup.find("form").find_next("legend").get_text()
    assert title == "H4x0rs Only - Step 2/2"

    question_text = (
        soup.find_all("div", {"class": "alert-success"})[0].get_text().strip()
    )
    assert question_text == "yes or no?"


def test_dashboard_post_question_errors(db, client):
    response = client.get(reverse("question"), follow=True)
    assert response.status_code == 200
    assert response.redirect_chain == [("/d4shb04rd-f0r-1337/login/", 302)]

    response = client.post(reverse("question"), data={}, follow=True)
    assert response.status_code == 200
    assert response.redirect_chain == [("/d4shb04rd-f0r-1337/login/", 302)]

    # Identify the member
    client.post(reverse("login"), data={"username": "john"})

    response = client.post(reverse("question"), data={"foo": "bar"}, follow=True)
    soup = BeautifulSoup(response.content.decode(), features="html.parser")
    text = soup.find(id="error_1_id_answer").find_next("strong").get_text()
    assert text == "This field is required."

    response = client.post(reverse("question"), data={"answer": "foobar"}, follow=True)
    soup = BeautifulSoup(response.content.decode(), features="html.parser")
    text = soup.find_all("div", {"class": "alert-danger"})[0].find_next("p").get_text()
    assert response.status_code == 200
    assert response.redirect_chain == [("/d4shb04rd-f0r-1337/login/", 302)]
    assert text == "Bad answer"


def test_dashboard_post_question_success(db, client):
    client.post(reverse("login"), data={"username": "john"}, follow=True)
    response = client.post(reverse("question"), data={"answer": "yes"}, follow=True)
    soup = BeautifulSoup(response.content.decode(), features="html.parser")
    assert response.status_code == 200
    assert response.redirect_chain == [("/d4shb04rd-f0r-1337/profile/", 302)]
    text = soup.find(id="profile").find_next("h2").get_text()
    assert text == "Welcome john"
