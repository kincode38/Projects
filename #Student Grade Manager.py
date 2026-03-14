#Student Grade Manager
#Getting student scores
student_scores =input("Enter student scores separated by commas: ")
scores = [int(score) for score in student_scores.split(",")]
#Assigning grades using list comparehension
grades = ["A" if score >=90 else
          "B" if score >=80 else
          "C" if score >=70 else
          "D" if score >=60 else
          "F" 
          for score in scores
          ]
#filter passing on failing students
passing_students = [score for score in scores if score >=60]
failing_students = [score for score in scores if score <60]

#Print results
print("\n---Student Grades---")
for i,(score,grades)in enumerate(zip(scores,grades),start=1):
    print(f"Student {i}: Score={score}, Grade={grades}")
print("\n---Passing and failing students")
print("Passing Students:", passing_students)
print("Failing_students:", failing_students)