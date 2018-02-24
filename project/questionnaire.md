## ETL Architecture Project Questionnaire

### Project Data Points
1. Across all reservation partners for January & February, how many completed reservations occurred?

Found answer by the following query:
select count(*) from peerfit_project where signed_in_at between '2018-01-01 00:00:00' and '2018-03-01 00:00:00';
Output:
+----------+
| count(*) |
+----------+
|      126 |
+----------+


2. Which studio has the highest rate of reservation abandonement (did not cancel but did not check-in)?

Found answer by the following query:
select studio_key, count(*) as reservation_abandonment from peerfit_project where signed_in_at = '0000-00-00 00:00:00' and canceled = 0 group by studio_key order by reservation_abandonment desc;
Output:
+-------------------------------------+-------------------------+
| studio_key                          | reservation_abandonment |
+-------------------------------------+-------------------------+
| orlando-yoga                        |                       3 |
| crossfit-control-jacksonville-beach |                       2 |
| flushing-crossfit                   |                       2 |
| the-pilates-center                  |                       1 |
| prana-yoga                          |                       1 |
| hive-athletics                      |                       1 |
| true-grit-fitness                   |                       1 |
| power-yoga                          |                       1 |
| dance-trance-fitness                |                       1 |
| yoga-pose                           |                       1 |
| soho-cycling                        |                       1 |
+-------------------------------------+-------------------------+

3. Which fitness area (i.e., tag) has the highest number of completed reservations for February?

Found answer by the following query:
select class_tag, count(*) as completed_reservation from peerfit_project where signed_in_at between '2018-02-01 00:00:00' and '2018-03-01 00:00:00' group by class_tag order by completed_reservation desc;
Output:
+-----------+-----------------------+
| class_tag | completed_reservation |
+-----------+-----------------------+
| yoga      |                    12 |
| strength  |                    10 |
| pilates   |                     9 |
| crossfit  |                     5 |
| endurance |                     2 |
+-----------+-----------------------+

4. How many members completed at least 1 reservation and had no more than 1 canceled reservation in January?

Found answer by the following query:
select count(distinct member_id) from peerfit_project where reserved_for between '2018-01-01 00:00:00' and '2018-02-01 00:00:00' and canceled = 0;
Output:
+---------------------------+
| count(distinct member_id) |
+---------------------------+
|                        24 |
+---------------------------+



### Project Discussion
1. Describe what custom logic you chose to implement in your ETL solution and why?
The logic that I used was pretty straight forward in the sense that I knew that I could extract data from the csvs with the python library csv. Next I wanted to make sure that data was validated and transformed by checking with a method for each type of csv. I noticed that len of a valid row in club_ready csvs was 8 and for mbo it was 12, so that was my first check. Once data was transformed, it was just a matter of inserting the data into the database. One thing I handled in the Insertion of data was to further validate it with ternaries for canceled, so that the data was posted correctly.

2. What forecasting opportunities do you see with a dataset like this and why?
We can forecast which studios are most likely to be used based on the number of visits. Also, one thought is that we can predict our users engagement on the Peerfit platform by how quickly they are making their reservations. If there is a short duration between user login, viewing classes, and making reservations, then perhaps we can build out features in app that would increase their engage with the app. Ie. Nutrition articles to stay healthy(lose weight), fitness articles on key areas of the body that people are focused on improving(abs, hips, etc.)

3. What other data would you propose we gather to make reporting/forecasting more robust and why?
There are a myriad of questions that we could ask users on sign up or daily use to help them accomplish their fitness goals. For instance, I would ask users their personal preferences of what they want to improve on with their fitness goals. Then we could attract/retain new fitness studios that focus on those goals, pitched by data accrued in app.

4. What was difficult and how might you have approached that obstacle differently next time?
Dealing with NULL datetime objects can sometimes be difficult, so I would make sure that the data being stored from a request.POST is always validated and stored correctly. For instance, in one application that I created, I had to get a datetime value in a specific format to consume a third-party API.

The code that I wrote on the backend was like:
start_time = dateparser.parse(data[9])
time_tpl = '%Y-%m-%dT%H:%M:%S+00:00'
stfmt = start_time.strftime(time_tpl)

On the front end, I believe I used datepicker js library to make user input easy.

Using these steps ensured that I always passed the correct format to the API, but the same could be done in your application(if not already done), to ensure that data is stored correctly.
