%-------- Facts -----------
default_gpa(32).


% ------ Facts for grade points
% Grade points for exact letter grades
grade_point('A+', 4.3).
grade_point('A', 4.0).
grade_point('A-', 3.67).
grade_point('B+', 3.33).
grade_point('B', 3.0).
grade_point('B-', 2.67).
grade_point('C+', 2.33).
grade_point('C', 2.0).
grade_point('D+', 1.67).
grade_point('D-', 1.3).
grade_point('U', 0).

% Rules for determining grade ranges
grade_point(Score, Grade) :-
    Score >= 4.3,
    Grade = 'A+'.

grade_point(Score, Grade) :-
    Score >= 4.0, Score < 4.3,
    Grade = 'A'.

grade_point(Score, Grade) :-
    Score >= 3.67, Score < 4.0,
    Grade = 'A-'.

grade_point(Score, Grade) :-
    Score >= 3.33, Score < 3.67,
    Grade = 'B+'.

grade_point(Score, Grade) :-
    Score >= 3.0, Score < 3.33,
    Grade = 'B'.

grade_point(Score, Grade) :-
    Score >= 2.67, Score < 3.0,
    Grade = 'B-'.

grade_point(Score, Grade) :-
    Score >= 2.33, Score < 2.67,
    Grade = 'C+'.

grade_point(Score, Grade) :-
    Score >= 2.0, Score < 2.33,
    Grade = 'C'.

grade_point(Score, Grade) :-
    Score >= 1.67, Score < 2.0,
    Grade = 'D+'.

grade_point(Score, Grade) :-
    Score >= 1.3, Score < 1.67,
    Grade = 'D-'.

grade_point(Score, Grade) :-
    Score < 1.3,
    Grade = 'U'.
  
   
% Rule to calculate the total credits earned per semester
calculate_total_credits([], 0). % Base Case
% Recursive case: Compute the total number of credit per semester
calculate_total_credits([C|Credits], Total) :-
   calculate_total_credits(Credits, SumTail),
   Total is C + SumTail.


calculate_sum_GP_semester([], [], 0).
calculate_sum_GP_semester([C|Credits], [G|GradePoints], Total) :-
    WeightedGrade is C * G,
    calculate_sum_GP_semester(Credits, GradePoints, SumTail),
    Total is WeightedGrade + SumTail.


calculate_total_grade_points([], 0).
calculate_total_grade_points([G|GradePoints], Total) :-
   calculate_total_grade_points(GradePoints, SumTail),
   Total is (G + SumTail).


calculate_semester_GPA(SumGP, SumCred, GPA) :-
   GPA is (SumGP/SumCred).

calculate_cumulative_GPA(X, Y, Z) :-
   Z is (X / Y).

