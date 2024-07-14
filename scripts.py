import random

from datacenter.models import (
    Chastisement,
    Commendation,
    Lesson,
    Mark,
    Schoolkid,
    Subject,
)


def get_schoolkid(name):
    try:
        return Schoolkid.objects.get(full_name__contains=name)
    except Schoolkid.MultipleObjectsReturned:
        print(f"Школьников с именем {name} несколько, уточни запрос")
        return
    except Schoolkid.DoesNotExist:
        print("Такого школьника нет, уточни запрос")
        return


def fix_marks(schoolkid):
    Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(
        points="5"
    )


def remove_chastisements(schoolkid):
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(schoolkid, subject_title=None):
    commendation_variants = [
        "Молодец!",
        "Отлично!",
        "Хорошо!",
        "Гораздо лучше, чем я ожидал!",
        "Ты меня приятно удивил!",
        "Великолепно!",
        "Прекрасно!",
        "Ты меня очень обрадовал!",
        "Именно этого я давно ждал от тебя!",
        "Сказано здорово – просто и ясно!",
        "Ты, как всегда, точен!",
        "Очень хороший ответ!",
        "Талантливо!",
        "Ты сегодня прыгнул выше головы!",
        "Я поражен!",
        "Уже существенно лучше!",
        "Потрясающе!",
        "Замечательно!",
        "Прекрасное начало!",
        "Так держать!",
        "Ты на верном пути!",
        "Здорово!",
        "Это как раз то, что нужно!",
        "Я тобой горжусь!",
        "С каждым разом у тебя получается всё лучше!",
        "Мы с тобой не зря поработали!",
        "Я вижу, как ты стараешься!",
        "Ты растешь над собой!",
        "Ты многое сделал, я это вижу!",
        "Теперь у тебя точно все получится!",
    ]

    if subject_title:
        try:
            subject = Subject.objects.get(
                title__contains=subject_title,
                year_of_study=schoolkid.year_of_study,
            )
        except Subject.DoesNotExist:
            print("Такого предмета нет, видимо ошибка в написании")
            return
    else:
        subject = (
            Subject.objects.filter(year_of_study=schoolkid.year_of_study)
            .order_by("?")
            .first()
        )

    commendation_text = random.choice(commendation_variants)

    lesson = (
        Lesson.objects.filter(
            year_of_study=schoolkid.year_of_study,
            group_letter=schoolkid.group_letter,
            subject=subject,
        )
        .order_by("-date")
        .first()
    )

    Commendation.objects.update_or_create(
        created=lesson.date,
        schoolkid=schoolkid,
        subject=subject,
        teacher=lesson.teacher,
        defaults={"text": commendation_text},
    )
