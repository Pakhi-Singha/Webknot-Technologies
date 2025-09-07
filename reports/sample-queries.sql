-- Total registrations per event (popularity) in a college
SELECT
  e.event_id,
  e.title,
  e.type,
  COUNT(r.registration_id) AS registrations
FROM events e
LEFT JOIN registrations r ON r.event_id = e.event_id
WHERE e.college_id = :CollegeId
GROUP BY e.event_id, e.title, e.type
ORDER BY registrations DESC;

-- Total registrations per event *of a given type* 
SELECT
  e.event_id,
  e.title,
  e.type,
  COUNT(r.registration_id) AS registrations
FROM events e
LEFT JOIN registrations r ON r.event_id = e.event_id
WHERE e.college_id = :CollegeId
  AND e.type = :EventType --Give type
GROUP BY e.event_id, e.title, e.type
ORDER BY registrations DESC;

-- Attendance percentage for an event
WITH counts AS (
  SELECT
    (SELECT COUNT(*) FROM registrations WHERE event_id = :EventId) AS regs,
    (SELECT COUNT(*) FROM attendance    WHERE event_id = :EventId) AS atts
)
SELECT
  regs,
  atts,
  ROUND(CASE WHEN regs = 0 THEN 0.0 ELSE (atts * 100.0) / regs END, 2) AS attendance_percent
FROM counts;

-- Average feedback for an event
SELECT ROUND(AVG(rating), 2) AS avg_feedback
FROM feedback
WHERE event_id = :EventId;

-- Student participation 
SELECT
  s.student_id,
  s.student_name,
  COUNT(a.attendance_id) AS events_attended
FROM students s
LEFT JOIN attendance a ON a.student_id = s.student_id
WHERE s.student_id = :StudentId
GROUP BY s.student_id, s.student_name;

-- Top N most active students in a college
SELECT
  s.student_id,
  s.student_name,
  COUNT(a.attendance_id) AS attended
FROM students s
JOIN attendance a ON a.student_id = s.student_id
WHERE s.college_id = :CollegeId
GROUP BY s.student_id, s.student_name
ORDER BY attended DESC
LIMIT :Limit;

-- Registrations aggregated by event 
SELECT
  e.type,
  COUNT(r.registration_id) AS registrations
FROM events e
LEFT JOIN registrations r ON r.event_id = e.event_id
WHERE e.college_id = :CollegeId
GROUP BY e.type
ORDER BY registrations DESC;
