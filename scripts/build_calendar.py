#!/usr/bin/env python3
"""
Builds a combined seminars.ics calendar from FAMU/FSU seminar & colloquium
sources. Runs weekly via GitHub Actions, which commits the regenerated
.ics file back into the repo; GitHub Pages then serves it at a stable URL
that Outlook/Google Calendar/Apple Calendar can subscribe to.

Each source has its own fetch_* function. If a source fails or changes its
HTML structure, that function must catch the error, print a warning, and
return an empty list -- it must NEVER crash the whole run.

Sources (15), in the order the ranking table gave them:
 1.  FAMU-FSU IME                          -- fetch_famu_fsu_dept_events
 2.  FSU Statistics Colloquia               -- fetch_stat_colloquia
 3.  FSU ACM Seminar (Fall 2026)            -- fetch_acm_seminar
 4.  FSU Criminology Events                 -- fetch_criminology_events
 5.  FSU Economics                          -- fetch_localist_ics
 6.  FSU Scientific Computing Seminars      -- fetch_sc_listing
     + Workshops (bonus, not in the 15 but kept from v1)
 7.  FSU AI Events                          -- fetch_localist_ics (filtered)
 8.  Translational Research Seminar Series  -- fetch_translational_seminar
 9.  FAMU CoPPS/IPH News & Events           -- fetch_famu_pharmacy_news
 10. FSU Computer Science Events            -- fetch_cs_events
 11. ICON-Health Events                     -- fetch_icon_health_events
 12. College of Medicine Seminar Series     -- fetch_com_seminar_series
 13. FAMU-FSU CEE                           -- fetch_famu_fsu_dept_events
 14. FAMU-FSU ECE                           -- fetch_famu_fsu_dept_events
 15. FSU Mathematics                        -- fetch_math_events
"""

import re
import sys
import hashlib
import datetime as dt

import requests
from bs4 import BeautifulSoup
from icalendar import Calendar, Event

try:
    from zoneinfo import ZoneInfo
    TZ = ZoneInfo("America/New_York")
except ImportError:  # pragma: no cover
    TZ = None

NOW = dt.datetime.now(TZ)
TODAY = NOW.date()
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; VMWLabSeminarBot/1.0; "
                  "+https://vmwhite.github.io/tools)"
}
TIMEOUT = 20
MONTHS = ("January|February|March|April|May|June|July|August|September|"
          "October|November|December")


def log(msg):
    print(msg, file=sys.stderr)


def make_uid(*parts):
    raw = "|".join(str(p) for p in parts)
    return hashlib.sha1(raw.encode("utf-8")).hexdigest() + "@vmwhite.github.io"


def infer_year(month, day, ref=TODAY):
    """For sources that give 'Month Day' with no year, assume the next
    occurrence of that date (this year if still upcoming, else next)."""
    for year in (ref.year, ref.year + 1):
        try:
            candidate = dt.date(year, month, day)
        except ValueError:
            continue
        if candidate >= ref - dt.timedelta(days=1):
            return candidate
    return None


MONTH_NUM = {m: i for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July",
     "August", "September", "October", "November", "December"], start=1)}
MONTH_NUM.update({
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "Jun": 6, "Jul": 7, "Aug": 8,
    "Sep": 9, "Sept": 9, "Oct": 10, "Nov": 11, "Dec": 12,
})


# ---------------------------------------------------------------------------
# Generic helper: FAMU-FSU College of Engineering department pages
# (Drupal). IME, CEE, and ECE all embed the same "Upcoming Events" grid
# widget: a heading, then a `.view-events-grid` block containing `.event`
# cards, each with a `.title a` link, `.event-date` ("August 19, 2026"),
# and an `.event-time` ("2:30pm-4:30pm"). Confirmed against live markup
# for IME, CEE, and ECE.
# ---------------------------------------------------------------------------
def fetch_famu_fsu_dept_events(path, heading_substr, source_label):
    url = f"https://eng.famu.fsu.edu{path}"
    events = []
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        heading = soup.find(lambda tag: tag.name in ("h2", "h3") and heading_substr in tag.get_text())
        if not heading:
            log(f"[{source_label}] Could not find '{heading_substr}' heading -- page structure may have changed")
            return events

        grid = heading.find_next(class_="view-events-grid")
        cards = grid.select(".event") if grid else []
        if not cards:
            log(f"[{source_label}] Could not find event cards -- page structure may have changed")
            return events

        for card in cards:
            link_tag = card.select_one(".title a")
            date_tag = card.select_one(".event-date")
            time_tag = card.select_one(".event-time")
            if not link_tag or not date_tag:
                continue
            title = link_tag.get_text(strip=True)
            link = requests.compat.urljoin(url, link_tag.get("href", ""))
            try:
                date_obj = dt.datetime.strptime(date_tag.get_text(strip=True), "%B %d, %Y").date()
            except ValueError:
                continue

            start, end, all_day = None, None, True
            if time_tag:
                time_match = re.search(
                    r"(\d{1,2}:\d{2}\s*[ap]m)\s*-\s*(\d{1,2}:\d{2}\s*[ap]m)",
                    time_tag.get_text(strip=True), re.I,
                )
                if time_match:
                    try:
                        start_t = dt.datetime.strptime(time_match.group(1).upper().replace(" ", ""), "%I:%M%p")
                        end_t = dt.datetime.strptime(time_match.group(2).upper().replace(" ", ""), "%I:%M%p")
                        start = dt.datetime.combine(date_obj, start_t.time(), TZ)
                        end = dt.datetime.combine(date_obj, end_t.time(), TZ)
                        all_day = False
                    except ValueError:
                        pass

            if all_day:
                if date_obj < TODAY - dt.timedelta(days=1):
                    continue
                events.append({"title": title, "start": date_obj, "end": None,
                                "all_day": True, "url": link, "source": source_label})
            else:
                if start < NOW - dt.timedelta(days=1):
                    continue
                events.append({"title": title, "start": start, "end": end,
                                "all_day": False, "url": link, "source": source_label})
    except Exception as e:
        log(f"[{source_label}] fetch failed: {e}")
    log(f"[{source_label}] {len(events)} events")
    return events


# ---------------------------------------------------------------------------
# Generic helper: FSU's central Localist calendar (calendar.fsu.edu).
# dept_slug -> department-level feed (confirmed working for Economics).
# query -> raw querystring appended to /calendar.ics for a filtered feed
# (e.g. event_types[]=95096 for the "Artificial Intelligence" tag used by
# FSU AI Events). The filtered form is best-effort/unverified.
# ---------------------------------------------------------------------------
def fetch_localist_ics(source_label, dept_slug=None, query=None, base="https://calendar.fsu.edu"):
    if dept_slug:
        url = f"{base}/department/{dept_slug}/calendar/ics"
    elif query:
        url = f"{base}/calendar.ics?{query}"
    else:
        raise ValueError("fetch_localist_ics needs dept_slug or query")

    events = []
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        r.raise_for_status()
        cal = Calendar.from_ical(r.content)
        for comp in cal.walk("VEVENT"):
            summary = str(comp.get("summary", "Untitled event"))
            dtstart = comp.get("dtstart").dt
            dtend = comp.get("dtend").dt if comp.get("dtend") else None
            link = str(comp.get("url", "")) or url
            all_day = not isinstance(dtstart, dt.datetime)
            if all_day:
                if dtstart < TODAY - dt.timedelta(days=1):
                    continue
                events.append({
                    "title": summary, "start": dtstart, "end": None,
                    "all_day": True, "url": link, "source": source_label,
                })
            else:
                if dtstart.tzinfo is None:
                    dtstart = dtstart.replace(tzinfo=TZ)
                if dtstart < NOW - dt.timedelta(days=1):
                    continue
                events.append({
                    "title": summary, "start": dtstart, "end": dtend,
                    "all_day": False, "url": link, "source": source_label,
                })
    except Exception as e:
        log(f"[{source_label}] Localist feed fetch failed ({url}): {e}")
    log(f"[{source_label}] {len(events)} events")
    return events


# ---------------------------------------------------------------------------
# FSU Scientific Computing -- seminars + workshops (Joomla site, confirmed
# NOT on FSU's Localist calendar). It's a paginated article-listing table:
# each row is a `th.list-title a` (title, linking to the full post, whose
# title embeds the talk date like "Colloquium with X (2026-04-22)") and a
# `td.list-date` cell ("April 22 2026" -- no comma).
# ---------------------------------------------------------------------------
def fetch_sc_listing(path, source_label):
    url = f"https://www.sc.fsu.edu{path}"
    events = []
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        table = soup.find("table")
        rows = table.find_all("tr") if table else []
        if not rows:
            log(f"[{source_label}] Could not find listing table -- page structure may have changed")
            return events

        for row in rows:
            link_tag = row.select_one(".list-title a") or row.find("a", href=True)
            date_tag = row.select_one(".list-date")
            if not link_tag or not date_tag:
                continue
            title = link_tag.get_text(strip=True)
            if not title:
                continue
            href = requests.compat.urljoin(url, link_tag["href"])
            try:
                date_obj = dt.datetime.strptime(date_tag.get_text(strip=True), "%B %d %Y").date()
            except ValueError:
                continue
            if date_obj < TODAY - dt.timedelta(days=1):
                continue

            events.append({
                "title": title, "start": date_obj, "end": None,
                "all_day": True, "url": href, "source": source_label,
            })
    except Exception as e:
        log(f"[{source_label}] fetch failed: {e}")
    seen, deduped = set(), []
    for e in events:
        key = (e["title"], str(e["start"]))
        if key not in seen:
            seen.add(key)
            deduped.append(e)
    log(f"[{source_label}] {len(deduped)} events")
    return deduped


# ---------------------------------------------------------------------------
# FSU Statistics Colloquia. Page currently lists only past speakers under
# season headers ("### Spring 2026" -> "- March 6 - Dr. ..."). We parse
# that format and keep only entries dated today or later. Once the
# department publishes an upcoming semester in the same format, it will
# start appearing automatically.
# ---------------------------------------------------------------------------
def fetch_stat_colloquia():
    url = "https://stat.fsu.edu/events/colloquia"
    events = []
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        lines = soup.get_text("\n", strip=True).split("\n")

        season_year = None
        for line in lines:
            season_match = re.match(r"(Spring|Fall|Summer)\s+(\d{4})", line)
            if season_match:
                season_year = int(season_match.group(2))
                continue
            entry_match = re.match(r"([A-Z][a-z]+)\.?\s+(\d{1,2})\s*-\s*(.+)", line)
            if entry_match and season_year:
                month_str, day_str, speaker = entry_match.groups()
                month = MONTH_NUM.get(month_str[:3].title())
                if not month:
                    continue
                try:
                    date_obj = dt.date(season_year, month, int(day_str))
                except ValueError:
                    continue
                if date_obj < TODAY - dt.timedelta(days=1):
                    continue
                events.append({
                    "title": f"Statistics Colloquium: {speaker}",
                    "start": date_obj, "end": None, "all_day": True,
                    "url": url, "source": "FSU Statistics Colloquia",
                })
    except Exception as e:
        log(f"[stat] fetch failed: {e}")
    log(f"[stat] {len(events)} events")
    return events


# ---------------------------------------------------------------------------
# FSU Applied & Computational Mathematics (ACM) Seminar.
# NOTE: this is a hand-maintained, semester-specific page
# (ACM_Seminar_F_2026.html). It will need its URL updated to the new
# semester's page once Spring 2027 goes up -- see README.
# Each week is an `article.seminar-card` with a `.seminar-date` div
# ("08/25" or "09/25 (changed date)") and one or more `<h3>` headings
# under `.seminar-main` (multiple on double-header weeks).
# ---------------------------------------------------------------------------
def fetch_acm_seminar(url="https://www.math.fsu.edu/~lee/ACM_Seminar_F_2026.html", assumed_year=2026):
    events = []
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        cards = soup.select("article.seminar-card")
        if not cards:
            log("[acm] Could not find seminar-card articles -- page structure may have changed")
            return events

        for card in cards:
            date_tag = card.select_one(".seminar-date")
            if not date_tag:
                continue
            date_match = re.match(r"(\d{1,2})/(\d{1,2})", date_tag.get_text(strip=True))
            if not date_match:
                continue
            month, day = int(date_match.group(1)), int(date_match.group(2))
            try:
                current_date = dt.date(assumed_year, month, day)
            except ValueError:
                continue
            if current_date < TODAY - dt.timedelta(days=1):
                continue

            for h3 in card.select(".seminar-main h3"):
                title = h3.get_text(strip=True)
                if not title or title.upper() in ("TBA", "NO SEMINAR"):
                    continue
                events.append({
                    "title": f"ACM Seminar: {title}", "start": current_date,
                    "end": None, "all_day": True, "url": url,
                    "source": "FSU ACM Seminar",
                })
    except Exception as e:
        log(f"[acm] fetch failed: {e}")
    log(f"[acm] {len(events)} events")
    return events


# ---------------------------------------------------------------------------
# FSU Criminology Events -- real RSS feed (tag: Events), but the tag is
# mostly used for retrospective news posts rather than forward listings,
# so expect this to surface rarely. We only keep items whose title/summary
# contains a parseable future date.
# ---------------------------------------------------------------------------
def fetch_criminology_events():
    url = "https://criminology.fsu.edu/taxonomy/term/21/feed"
    events = []
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        r.raise_for_status()
        try:
            soup = BeautifulSoup(r.content, "xml")
        except Exception:
            soup = BeautifulSoup(r.content, "html.parser")
        for item in soup.find_all("item"):
            title = item.find("title").get_text(strip=True) if item.find("title") else None
            link = item.find("link").get_text(strip=True) if item.find("link") else url
            desc = item.find("description").get_text(" ", strip=True) if item.find("description") else ""
            if not title:
                continue
            m = re.search(r"(\d{1,2})/(\d{1,2})/(\d{2,4})", title + " " + desc)
            date_obj = None
            if m:
                mo, da, yr = m.groups()
                yr = int(yr) if len(yr) == 4 else 2000 + int(yr)
                try:
                    date_obj = dt.date(yr, int(mo), int(da))
                except ValueError:
                    date_obj = None
            if not date_obj:
                m2 = re.search(rf"({MONTHS})\s+(\d{{1,2}}),?\s*(\d{{4}})", title + " " + desc)
                if m2:
                    month_str, day_str, year_str = m2.groups()
                    month = MONTH_NUM.get(month_str)
                    if month:
                        try:
                            date_obj = dt.date(int(year_str), month, int(day_str))
                        except ValueError:
                            date_obj = None
            if not date_obj or date_obj < TODAY - dt.timedelta(days=1):
                continue
            events.append({
                "title": title, "start": date_obj, "end": None, "all_day": True,
                "url": link, "source": "FSU Criminology Events",
            })
    except Exception as e:
        log(f"[criminology] fetch failed: {e}")
    log(f"[criminology] {len(events)} events")
    return events


# ---------------------------------------------------------------------------
# FSU Computer Science Events (WordPress/Tribe-style). Page has an
# "Upcoming Events" section followed by "Past Events" -- we only read the
# upcoming one. Each item is an <h2> link like "Talk Title (Apr 22)"
# followed by a "Date April 22, 10:00 AM" or "Date: Feb 27, 11:15 - 12:15
# pm" line with no year given, so we infer the nearest future occurrence.
# ---------------------------------------------------------------------------
def fetch_cs_events():
    url = "https://www.cs.fsu.edu/events/"
    events = []
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        upcoming_heading = soup.find(lambda tag: tag.name in ("h1", "h2", "h3", "strong") and "Upcoming Events" in tag.get_text())
        past_heading = soup.find(lambda tag: tag.name in ("h1", "h2", "h3", "strong") and "Past Events" in tag.get_text())
        if not upcoming_heading:
            log("[cs] Could not find 'Upcoming Events' heading -- page structure may have changed")
            return events

        node = upcoming_heading.find_next_sibling()
        while node and node is not past_heading:
            link_tag = node.find("a", href=True) if hasattr(node, "find") else None
            if link_tag:
                title = link_tag.get_text(strip=True)
                href = requests.compat.urljoin(url, link_tag["href"])
                block_text = node.get_text(" ", strip=True)
                m = re.search(rf"Date:?\s*({MONTHS}|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\s+(\d{{1,2}})", block_text, re.I)
                if m:
                    month = MONTH_NUM.get(m.group(1).title()) or MONTH_NUM.get(m.group(1)[:3].title())
                    day = int(m.group(2))
                    if month:
                        date_obj = infer_year(month, day)
                        if date_obj:
                            events.append({
                                "title": title, "start": date_obj, "end": None,
                                "all_day": True, "url": href,
                                "source": "FSU Computer Science Events",
                            })
            node = node.find_next_sibling()
    except Exception as e:
        log(f"[cs] fetch failed: {e}")
    log(f"[cs] {len(events)} events")
    return events


# ---------------------------------------------------------------------------
# ICON-Health Events & Convenings. This is a free-text prose page, not a
# structured listing -- best-effort only. We pull each <h2> whose text (or
# the paragraph right after it) contains a recognizable date, and use the
# first date found as the event date. Expect this to need the occasional
# manual look since the page is written narratively.
# ---------------------------------------------------------------------------
def fetch_icon_health_events():
    url = "https://icon.fsu.edu/events-convenings"
    events = []
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        for heading in soup.find_all(["h2", "h3"]):
            title = heading.get_text(strip=True)
            if not title or "Events & Convenings" in title:
                continue
            search_text = title
            sib = heading.find_next_sibling()
            if sib:
                search_text += " " + sib.get_text(" ", strip=True)

            m = re.search(rf"({MONTHS})\s+(\d{{1,2}})(?:-\d{{1,2}})?", search_text)
            if not m:
                continue
            month = MONTH_NUM.get(m.group(1))
            day = int(m.group(2))
            date_obj = infer_year(month, day)
            if not date_obj:
                continue
            events.append({
                "title": title, "start": date_obj, "end": None, "all_day": True,
                "url": url, "source": "ICON-Health Events",
            })
    except Exception as e:
        log(f"[icon-health] fetch failed: {e}")
    log(f"[icon-health] {len(events)} events")
    return events


# ---------------------------------------------------------------------------
# College of Medicine Seminar Series. med.fsu.edu/calendar/fulldisplay/all
# is a structured Date/Title/Location/Event Type table covering ALL
# College of Medicine events (commencements, alumni events, etc.) -- we
# filter to rows where Event Type is "Seminar" or the title contains
# "Seminar", and keep only future dates.
# ---------------------------------------------------------------------------
def fetch_com_seminar_series():
    url = "https://med.fsu.edu/calendar/fulldisplay/all"
    events = []
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.find("table")
        if not table:
            log("[com-seminar] Could not find events table -- page structure may have changed")
            return events

        rows = table.find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            if len(cells) < 2:
                continue
            date_text = cells[0].get_text(strip=True)
            title_link = cells[1].find("a", href=True)
            if not title_link:
                continue
            title = title_link.get_text(strip=True)
            href = requests.compat.urljoin(url, title_link["href"])
            event_type = cells[3].get_text(strip=True) if len(cells) > 3 else ""

            if "seminar" not in event_type.lower() and "seminar" not in title.lower():
                continue

            m = re.match(r"(\w{3})\s+(\d{1,2}),?\s*(\d{4})", date_text)
            if not m:
                continue
            month_str, day_str, year_str = m.groups()
            month = MONTH_NUM.get(month_str.title())
            if not month:
                continue
            try:
                date_obj = dt.date(int(year_str), month, int(day_str))
            except ValueError:
                continue
            if date_obj < TODAY - dt.timedelta(days=1):
                continue

            events.append({
                "title": title, "start": date_obj, "end": None, "all_day": True,
                "url": href, "source": "College of Medicine Seminar Series",
            })
    except Exception as e:
        log(f"[com-seminar] fetch failed: {e}")
    log(f"[com-seminar] {len(events)} events")
    return events


# ---------------------------------------------------------------------------
# Translational Research Seminar Series. This is a single, hand-written
# announcement article with a bullet schedule:
#   "**October 17, 2025 12:30 - 1:30**" followed by a title line.
# NOTE: this URL is specific to the 2025-2026 run of the series -- a new
# run will likely get a new announcement URL, which will need updating
# here. See README.
# ---------------------------------------------------------------------------
def fetch_translational_seminar():
    url = "https://announcements.fsu.edu/article/register-now-translational-research-seminar-series"
    events = []
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        for bold in soup.find_all(["strong", "b"]):
            text = bold.get_text(strip=True)
            m = re.match(rf"({MONTHS})\s+(\d{{1,2}}),\s*(\d{{4}})", text)
            if not m:
                continue
            month_str, day_str, year_str = m.groups()
            month = MONTH_NUM.get(month_str)
            try:
                date_obj = dt.date(int(year_str), month, int(day_str))
            except (ValueError, TypeError):
                continue
            if date_obj < TODAY - dt.timedelta(days=1):
                continue

            title = "Translational Research Seminar"
            li = bold.find_parent("li")
            if li:
                next_text = li.find_next_sibling()
                if next_text:
                    candidate = next_text.get_text(strip=True)
                    if candidate:
                        title = f"Translational Research Seminar: {candidate}"

            events.append({
                "title": title, "start": date_obj, "end": None, "all_day": True,
                "url": url, "source": "Translational Research Seminar",
            })
    except Exception as e:
        log(f"[translational] fetch failed: {e}")
    log(f"[translational] {len(events)} events")
    return events


# ---------------------------------------------------------------------------
# FAMU Institute of Public Health / College of Pharmacy. This is a general
# news feed, not a seminar calendar -- most stories have no date/time.
# Only pick up stories with an explicit "Month Day, Year | time" pattern.
# ---------------------------------------------------------------------------
def fetch_famu_pharmacy_news():
    url = "https://pharmacy.famu.edu/news/News.php"
    events = []
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        for card in soup.select("h3, h2"):
            link_tag = card.find("a", href=True)
            if not link_tag:
                continue
            title = link_tag.get_text(strip=True)
            context = card.find_parent()
            context_text = context.get_text(" ", strip=True) if context else ""
            m = re.search(
                rf"({MONTHS})\s+(\d{{1,2}}),\s*(\d{{4}})"
                r"(?:\s*\|\s*(\d{1,2}:\d{2}\s*[ap]\.?m\.?))?",
                context_text, re.I,
            )
            if not m:
                continue
            month_str, day, year, _time_str = m.groups()
            month = MONTH_NUM.get(month_str)
            if not month:
                continue
            try:
                date_obj = dt.date(int(year), month, int(day))
            except ValueError:
                continue
            if date_obj < TODAY - dt.timedelta(days=1):
                continue
            href = requests.compat.urljoin(url, link_tag["href"])
            events.append({
                "title": title, "start": date_obj, "end": None, "all_day": True,
                "url": href, "source": "FAMU IPH / Pharmacy",
            })
    except Exception as e:
        log(f"[pharmacy] fetch failed: {e}")
    log(f"[pharmacy] {len(events)} events")
    return events


# ---------------------------------------------------------------------------
# FSU Mathematics -- mathematics.fsu.edu/events (Drupal). Currently empty
# ("no upcoming events"); structure mirrors the FAMU-FSU Engineering event
# pages, so we reuse a similar title-link + date-line pattern generically.
# ---------------------------------------------------------------------------
def fetch_math_events():
    url = "https://mathematics.fsu.edu/events"
    events = []
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        if "no upcoming events" in soup.get_text(" ", strip=True).lower():
            log("[math] 0 events (page reports none currently scheduled)")
            return events

        for link_tag in soup.select("main a[href*='/event']"):
            title = link_tag.get_text(strip=True)
            if not title:
                continue
            container = link_tag.find_parent(["article", "div", "li"]) or link_tag.parent
            block_text = container.get_text(" ", strip=True) if container else ""
            m = re.search(rf"({MONTHS})\s+(\d{{1,2}}),?\s*(\d{{4}})", block_text)
            if not m:
                continue
            month_str, day_str, year_str = m.groups()
            month = MONTH_NUM.get(month_str)
            try:
                date_obj = dt.date(int(year_str), month, int(day_str))
            except (ValueError, TypeError):
                continue
            if date_obj < TODAY - dt.timedelta(days=1):
                continue
            href = requests.compat.urljoin(url, link_tag["href"])
            events.append({
                "title": title, "start": date_obj, "end": None, "all_day": True,
                "url": href, "source": "FSU Mathematics",
            })
    except Exception as e:
        log(f"[math] fetch failed: {e}")
    log(f"[math] {len(events)} events")
    return events


# ---------------------------------------------------------------------------
# Assemble everything into one .ics
# ---------------------------------------------------------------------------
def build_calendar(all_events):
    cal = Calendar()
    cal.add("prodid", "-//VMW Lab Seminar Calendar//vmwhite.github.io//")
    cal.add("version", "2.0")
    cal.add("x-wr-calname", "VMW Lab Seminar & Colloquium Calendar")
    cal.add("x-wr-timezone", "America/New_York")
    cal.add(
        "x-wr-caldesc",
        "Auto-updated weekly. 15 FAMU/FSU seminar, colloquium, and event sources.",
    )

    for e in all_events:
        ev = Event()
        ev.add("summary", f"[{e['source']}] {e['title']}")
        ev.add("uid", make_uid(e["source"], e["title"], e["start"]))
        ev.add("dtstamp", NOW)
        ev.add("dtstart", e["start"])
        if not e["all_day"] and e.get("end"):
            ev.add("dtend", e["end"])
        if e.get("url"):
            ev.add("url", e["url"])
            ev.add("description", e["url"])
        cal.add_component(ev)

    return cal


def main():
    all_events = []

    # 1. FAMU-FSU IME
    all_events += fetch_famu_fsu_dept_events("/ime", "IME Events", "FAMU-FSU IME")
    # 2. FSU Statistics Colloquia
    all_events += fetch_stat_colloquia()
    # 3. FSU ACM Seminar
    all_events += fetch_acm_seminar()
    # 4. FSU Criminology Events
    all_events += fetch_criminology_events()
    # 5. FSU Economics
    all_events += fetch_localist_ics("FSU Economics", dept_slug="economics")
    # 6. FSU Scientific Computing Seminars (+ bonus: Workshops)
    all_events += fetch_sc_listing("/news-and-events/seminars", "FSU Scientific Computing Seminars")
    all_events += fetch_sc_listing("/news-and-events/workshops", "FSU Scientific Computing Workshops")
    # 7. FSU AI Events (Localist, filtered by tag -- best-effort/unverified slug)
    all_events += fetch_localist_ics("FSU AI Events", query="event_types%5B%5D=95096")
    # 8. Translational Research Seminar Series
    all_events += fetch_translational_seminar()
    # 9. FAMU CoPPS/IPH News & Events
    all_events += fetch_famu_pharmacy_news()
    # 10. FSU Computer Science Events
    all_events += fetch_cs_events()
    # 11. ICON-Health Events
    all_events += fetch_icon_health_events()
    # 12. College of Medicine Seminar Series
    all_events += fetch_com_seminar_series()
    # 13. FAMU-FSU CEE
    all_events += fetch_famu_fsu_dept_events("/cee", "CEE Events", "FAMU-FSU CEE")
    # 14. FAMU-FSU ECE
    all_events += fetch_famu_fsu_dept_events("/ece", "ECE Events", "FAMU-FSU ECE")
    # 15. FSU Mathematics
    all_events += fetch_math_events()

    cal = build_calendar(all_events)

    out_path = "tools/seminars.ics"
    with open(out_path, "wb") as f:
        f.write(cal.to_ical())

    log(f"\nWrote {len(all_events)} total events to {out_path}")


if __name__ == "__main__":
    main()
