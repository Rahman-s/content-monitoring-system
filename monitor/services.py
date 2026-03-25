import json
import os

from django.utils.dateparse import parse_datetime

from .models import Keyword, ContentItem, Flag


def normalize_text(text):
    return text.lower().strip()


def calculate_score(keyword_name, title, body):
    keyword = normalize_text(keyword_name)
    title_text = normalize_text(title)
    body_text = normalize_text(body)

    title_words = title_text.split()

    # Exact keyword word present in title
    if keyword in title_words:
        return 100

    # Partial keyword match in title
    if keyword in title_text:
        return 70

    # Keyword appears in body only
    if keyword in body_text:
        return 40

    return 0


def load_mock_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'mock_data.json')

    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def import_content_items():
    data = load_mock_data()
    imported_items = []

    for item in data:
        content_item, created = ContentItem.objects.update_or_create(
            title=item['title'],
            source=item['source'],
            defaults={
                'body': item['body'],
                'last_updated': parse_datetime(item['last_updated'])
            }
        )
        imported_items.append(content_item)

    return imported_items


def should_create_or_update_flag(keyword, content_item, score):
    try:
        existing_flag = Flag.objects.get(keyword=keyword, content_item=content_item)

        # If reviewer marked it irrelevant, suppress until content changes
        if existing_flag.status == 'irrelevant':
            if existing_flag.suppressed_at_content_update == content_item.last_updated:
                return None

            # Content changed -> show again as pending
            existing_flag.score = score
            existing_flag.status = 'pending'
            existing_flag.suppressed_at_content_update = None
            existing_flag.save()
            return existing_flag

        # If already pending/relevant, just refresh score
        existing_flag.score = score
        existing_flag.save()
        return existing_flag

    except Flag.DoesNotExist:
        return Flag.objects.create(
            keyword=keyword,
            content_item=content_item,
            score=score,
            status='pending'
        )


def run_scan():
    keywords = Keyword.objects.all()
    content_items = import_content_items()

    created_or_updated_flags = []

    for keyword in keywords:
        for content_item in content_items:
            score = calculate_score(keyword.name, content_item.title, content_item.body)

            if score > 0:
                flag = should_create_or_update_flag(keyword, content_item, score)
                if flag is not None:
                    created_or_updated_flags.append(flag)

    return created_or_updated_flags