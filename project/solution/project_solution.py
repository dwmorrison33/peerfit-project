import MySQLdb
import sys
import csv
import glob


def connect_to_db(hostname, username, password, database):
    db = MySQLdb.connect(
        host=hostname,
        user=username,
        passwd=password,
        db=database
    )
    cursor = db.cursor()
    table_name = "peerfit_project"
    cursor.execute("DROP TABLE IF EXISTS {}".format(table_name))
    # Below, I made zip an varchar cause they sometimes contain a minus sign
    cursor.execute("""CREATE TABLE {} (
        member_id INT(5) NOT NULL,
        studio_key VARCHAR(255) NOT NULL,
        class_tag VARCHAR(255) NOT NULL,
        instructor_full_name VARCHAR(255),
        level INT(5),
        canceled BOOL NOT NULL,
        reserved_for DATETIME,
        signed_in_at DATETIME,
        studio_address_street VARCHAR(255),
        studio_address_city VARCHAR(255),
        studio_address_state VARCHAR(255),
        studio_address_zip VARCHAR(20),
        viewed_at DATETIME,
        reserved_at DATETIME
    );
    """.format(table_name))
    db.commit()
    return db, cursor

def row_from_club_ready_csv_is_valid(data):
    """
        NOTE, all invalid datetimes will be NULL in db
        NULL datetime values are stored in db like 0000-00-00 00:00:00
    """
    # valid data has a length of 8
    if len(data) != 8:
        # need to log errant data to error.log
        return False
    else:
        return True

def transform_club_ready_csv_data(data):
    """
        data is a list of lists, we are gonna iterate over those
        lists to formulate data into a list of dicts to store in db
    """
    column_names = data[0]
    all_data = []
    updated_data = {}

    for d in data[1:]:
        if row_from_club_ready_csv_is_valid(d):
            for i in range(8):
                updated_data.update({column_names[i]: d[i]})
            all_data.append(updated_data)
            updated_data = {}

    return all_data

def row_from_mbo_csv_is_valid(data):
    """
        NOTE, all invalid datetimes will be NULL in db
        NULL datetime values are stored in db like 0000-00-00 00:00:00
    """
    # valid data has a length of 12
    if len(data) != 12:
        # need to log data to error.log
        return False
    # must have a value for first index
    if not data[0]:
        # need to log errant data to error.log
        return False
    else:
        return True

def transform_mbo_csv_data(data):
    """
        data is a list of lists, we are gonna iterate over those
        lists to formulate data into a list of dicts to store in db
    """
    column_names = data[0]
    all_data = []
    updated_data = {}

    for d in data[1:]:
        if row_from_mbo_csv_is_valid(d):
            for i in range(12):
                updated_data.update({column_names[i]: d[i]})
            all_data.append(updated_data)
            updated_data = {}

    return all_data


def scrape_files(db, cursor, file_names):
    """
        Here we will read files with the csv modules and
        get the validated and transformed data and load into db
    """

    table_name = "peerfit_project"
    for file_name in file_names:
        file = open(file_name, 'rb')
        csv_reader = csv.reader(file)
        all_data = list(csv_reader)

        if 'club' in file_name:
            validated_data = transform_club_ready_csv_data(all_data)
            for vd in validated_data:
                cursor.execute("""
                    INSERT INTO {} (
                        member_id,
                        studio_key,
                        class_tag,
                        instructor_full_name,
                        level,
                        canceled,
                        reserved_for,
                        signed_in_at)
                    VALUES ({}, '{}', '{}', '{}', '{}', {}, '{}', '{}')
                    """.format(
                        table_name,
                        int(vd['member_id']),
                        vd['studio_key'],
                        vd['class_tag'],
                        vd['instructor_full_name'],
                        vd['level'],
                        "False" if vd['canceled'] == "f" else "True",
                        vd['reserved_for'],
                        vd['signed_in_at'],
                    ))
            db.commit()

        if 'mbo' in file_name:
            validated_data = transform_mbo_csv_data(all_data)
            for vd in validated_data:
                cursor.execute("""
                    INSERT INTO {} (
                        member_id,
                        studio_key,
                        class_tag,
                        canceled,
                        reserved_for,
                        signed_in_at,
                        studio_address_street,
                        studio_address_city,
                        studio_address_state,
                        studio_address_zip,
                        viewed_at,
                        reserved_at)
                    VALUES ({}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
                    """.format(
                        table_name,
                        int(vd['member_id']),
                        vd['studio_key'],
                        vd['class_tag'],
                        0 if not vd['canceled_at'] else 1,
                        vd['class_time_at'],
                        vd['checked_in_at'],
                        vd['studio_address_street'],
                        vd['studio_address_city'],
                        vd['studio_address_state'].replace(" ", ""),
                        vd['studio_address_zip'],
                        vd['viewed_at'],
                        vd['reserved_at'],
                    ))
            db.commit()

def main():
    if len(sys.argv) != 5:
        print("Usage: python <name_of_script> <host> <user> <password> <database>")
        sys.exit(1)

    hostname = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    database = sys.argv[4]

    db, cursor = connect_to_db(hostname, username, password, database)
    files_to_scrape = glob.glob('../data/*.csv')
    scrape_files(db, cursor, files_to_scrape)
    db.close()

if __name__ == "__main__":
    main()