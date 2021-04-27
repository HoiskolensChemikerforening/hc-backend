from django.db import models
from ckeditor.fields import RichTextField
from sorl.thumbnail import ImageField


class Specialization(models.Model):
    SPECIALIZATIONS = (
        (1, "Bioteknologi"),
        (2, "Organisk kjemi"),
        (3, "Anvendt teoretisk kjemi"),
        (4, "Analytisk kjemi"),
        (5, "Kjemisk prosessteknologi"),
        (6, "Materialkjemi og energiteknologi"),
    )

    name = models.PositiveSmallIntegerField(
        choices=SPECIALIZATIONS, unique=True
    )

    def __str__(self):
        return self.get_name_display()


class Interview(models.Model):
    title = models.CharField(max_length=40, verbose_name="Navn på intervjuet")
    text = RichTextField(verbose_name="Intervjuet", config_name="forms")
    picture = ImageField(upload_to="corporate", verbose_name="Bilde")
    company_picture = ImageField(
        upload_to="corporate",
        verbose_name="Logo til bedriften",
        blank=True,
        null=True,
    )
    specializations = models.ManyToManyField(
        Specialization, verbose_name="Aktuelle retninger", blank=True
    )
    graduation_year = models.PositiveSmallIntegerField(
        default=2000, verbose_name="Uteksamineringsår"
    )

    def __str__(self):
        return self.title


class JobAdvertisement(models.Model):
    title = models.CharField(max_length=100, verbose_name="Stilling")
    description = RichTextField(
        verbose_name="Beskrivelse", config_name="forms"
    )
    is_published = models.BooleanField(verbose_name="Er synlig", default=True)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Survey(models.Model):
    year = models.IntegerField(verbose_name="Årstall", unique=True)

    def get_q_a_dict(self):
        q_a_pairs = AnswerKeyValuePair.objects.filter(
            survey=self
        ).prefetch_related("question")
        q_a_dict = {}

        for q_a in q_a_pairs:
            q = q_a.question.question
            chart_type = q_a.question.chart_type
            answer = q_a.key
            id = q_a.id
            number_of_answers = q_a.value

            if q not in q_a_dict.keys():
                question_data = {
                    "ids": [id],
                    "choices": [answer],
                    "values": [number_of_answers],
                    "chartType": chart_type,
                }
                q_a_dict[q] = question_data
            else:
                q_a_dict[q]["ids"].append(id)
                q_a_dict[q]["choices"].append(answer)
                q_a_dict[q]["values"].append(number_of_answers)

        return q_a_dict

    def __str__(self):
        return "Diplomundersøkelsen fra " + str(self.year)


class SurveyQuestion(models.Model):
    BAR_CHART = "bar"
    PIE_CHART = "pie"

    PLOT_TYPE_CHOICES = [
        (BAR_CHART, "Bar chart"),
        (PIE_CHART, "Pie chart"),
    ]

    question = models.TextField(max_length=300, verbose_name="Spørsmål")
    chart_type = models.CharField(
        max_length=100,
        choices=PLOT_TYPE_CHOICES,
        default=BAR_CHART,
        verbose_name="Graftype",
    )

    def __str__(self):
        return self.question


class AnswerKeyValuePair(models.Model):
    key = models.TextField(max_length=300, verbose_name="Svaralternativ")
    value = models.IntegerField(verbose_name="Antall")
    question = models.ForeignKey(
        SurveyQuestion, on_delete=models.CASCADE, verbose_name="Spørsmål"
    )
    survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE, verbose_name="Undersøkelse"
    )

    def __str__(self):
        return (
            str(self.survey.year)
            + " - "
            + str(self.question.question)
            + ": "
            + str(self.key)
            + " - "
            + str(self.value)
        )
