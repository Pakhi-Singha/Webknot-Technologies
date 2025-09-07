-- Total registrations per event (popularity)
SELECT e.id, e.title, e.type, COUNT(r.id) AS registrations
FROM events e
LEFT JOIN registrations r ON r.event_id = e.id
WHERE e.college_id = :college_id
GROUP BY e.id
ORDER BY registrations DESC;

-- Attendance percentage for an event
WITH counts AS (
  SELECT
    (SELECT COUNT(*) FROM registrations WHERE event_id = :event_id) AS regs,
    (SELECT COUNT(*) FROM attendance    WHERE event_id = :event_id) AS atts
)
SELECT regs, atts, ROUND(CASE WHEN regs=0 THEN 0.0 ELSE (atts*100.0)/regs END, 2) AS attendance_percent
FROM counts;

-- Average feedback score
SELECT ROUND(AVG(rating), 2) AS avg_feedback
FROM feedback
WHERE event_id = :event_id;

-- Student participation (events attended)
SELECT s.id AS student_id, s.name, COUNT(a.id) AS events_attended
FROM students s
LEFT JOIN attendance a ON a.student_id = s.id
WHERE s.id = :student_id
GROUP BY s.id;

-- Top 3 most active students (by attendance)
SELECT s.id, s.name, COUNT(a.id) AS attended
FROM students s
JOIN attendance a ON a.student_id = s.id
WHERE s.college_id = :college_id
GROUP BY s.id
ORDER BY attended DESC
LIMIT 3;

-- Total registrations per event type (popularity)
SELECT 
    e.event_id, 
    e.title, 
    e.type, 
    COUNT(r.registration_id) AS registrations
FROM events e
LEFT JOIN registrations r 
    ON r.event_id = e.event_id
WHERE e.college_id = :CollegeId
  AND e.type = :EventType
GROUP BY e.event_id, e.title, e.type
ORDER BY registrations DESC;
