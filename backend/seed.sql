--Optional testing data

INSERT INTO colleges(id, name) VALUES (1,'Webknight College') ON CONFLICT DO NOTHING;

INSERT INTO students(id, college_id, name, email, year) VALUES
 (1,1,'Riya','riya@wk.edu','2'),
 (2,1,'Aasha','aasha@wk.edu','3'),
 (3,1,'Lucy','lucy@wk.edu','4');

INSERT INTO events(id, college_id, title, type, starts_at, ends_at) VALUES
 (1,1,'Intro to FastAPI','Workshop','2025-09-07 10:00:00','2025-09-07 12:00:00'),
 (2,1,'AI Tech Talk','Seminar','2025-09-07 14:00:00','2025-09-07 15:00:00');

INSERT INTO registrations(student_id,event_id,created_at) VALUES
 (1,1,CURRENT_TIMESTAMP),(2,1,CURRENT_TIMESTAMP),(3,1,CURRENT_TIMESTAMP),
 (1,2,CURRENT_TIMESTAMP),(2,2,CURRENT_TIMESTAMP);

INSERT INTO attendance(student_id,event_id,checked_in_at) VALUES
 (1,1,CURRENT_TIMESTAMP),(2,1,CURRENT_TIMESTAMP),
 (1,2,CURRENT_TIMESTAMP);

INSERT INTO feedback(student_id,event_id,rating,comment,created_at) VALUES
 (1,1,5,'Great workshop',CURRENT_TIMESTAMP),
 (2,1,4,'Good content',CURRENT_TIMESTAMP),
 (1,2,3,'Okay talk',CURRENT_TIMESTAMP);

