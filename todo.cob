       IDENTIFICATION DIVISION.
       PROGRAM-ID. TodoList.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  Task-List.
           05  Task-Count      PIC 9(3) VALUE 0.
           05  Tasks OCCURS 100.
               10  Task-Name      PIC X(50).
               10  Task-Status    PIC X(10).
       01  User-Input         PIC X(50).
       01  Display-Message    PIC X(100).

       PROCEDURE DIVISION.
       Main-Procedure.
           PERFORM Display-Menu.
           PERFORM UNTIL User-Input = "Q"
               DISPLAY Display-Message
               ACCEPT User-Input
               EVALUATE User-Input
                   WHEN "1"
                       PERFORM Add-Task
                   WHEN "2"
                       PERFORM View-Tasks
                   WHEN "3"
                       PERFORM Manage-Tasks
                   WHEN OTHER
                       DISPLAY "Invalid option!"
               END-EVALUATE
           END-PERFORM.
           DISPLAY "Exiting program..."
           STOP RUN.

       Display-Menu.
           DISPLAY "To-Do List Menu:"
           DISPLAY "1. Add Task"
           DISPLAY "2. View Tasks"
           DISPLAY "3. Manage Tasks"
           DISPLAY "Q. Quit".

       Add-Task.
           DISPLAY "Enter task name:"
           ACCEPT Task-Name
           MOVE Task-Name TO Tasks(Task-Count)
           MOVE "Pending" TO Task-Status OF Tasks(Task-Count)
           ADD 1 TO Task-Count.

       View-Tasks.
           DISPLAY "Task List:".
           PERFORM VARYING Index FROM 1 BY 1 UNTIL Index > Task-Count
               DISPLAY Tasks(Index). 
           END-PERFORM.

       Manage-Tasks.
           DISPLAY "Manage Tasks (Not Implemented)".
           
       END PROGRAM TodoList.
