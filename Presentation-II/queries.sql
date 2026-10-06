USE campus_placement;
-- Include departments with no offers. Count offers; dashboard counts distinct placed students.
SELECT d.dept_name, COUNT(p.placement_id) AS placed_count, MAX(p.package) AS top_package
FROM Department d
LEFT JOIN Student s ON s.dept_id=d.dept_id
LEFT JOIN Application a ON a.student_id=s.student_id
LEFT JOIN Placement p ON p.application_id=a.application_id
GROUP BY d.dept_id,d.dept_name ORDER BY placed_count DESC;
SELECT * FROM Student;
SELECT * FROM Application;
SELECT * FROM Placement;
