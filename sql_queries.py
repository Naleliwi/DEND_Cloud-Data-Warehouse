import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROPING TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATING TABLES


# Staging tables 

staging_events_table_create= ("""

CREATE TABLE  IF NOT EXISTS  staging_events (

        artist              VARCHAR,
        auth                VARCHAR,
        firstName           VARCHAR,
        gender              VARCHAR,
        itemInSession       INTEGER,
        lastName            VARCHAR,
        length              FLOAT,
        level               VARCHAR,
        location            VARCHAR,
        method              VARCHAR,
        page                VARCHAR,
        registration        FLOAT,
        sessionId           INTEGER,
        song                VARCHAR,
        status              INTEGER,
        ts                  BIGINT,
        userAgent           VARCHAR,
        userId              INTEGER 

);
""")

staging_songs_table_create = ("""

CREATE TABLE  IF NOT EXISTS staging_songs (

        num_songs           INTEGER,
        artist_id           VARCHAR,
        artist_latitude     FLOAT,
        artist_longitude    FLOAT,
        artist_location     VARCHAR,
        artist_name         VARCHAR,
        song_id             VARCHAR,
        title               VARCHAR NOT NULL,
        duration            FLOAT,
        year                INTEGER
        
);
""")

# Fact table 

songplay_table_create = ("""

CREATE TABLE songplays(

        songplay_id          INTEGER IDENTITY(0,1) PRIMARY KEY,
        start_time           TIMESTAMP,
        user_id              INTEGER,
        level                VARCHAR,
        song_id              VARCHAR,
        artist_id            VARCHAR,
        session_id           INTEGER,
        location             VARCHAR,
        user_agent           VARCHAR
        
);
""")

# Diminsional tables 

user_table_create = ("""

CREATE TABLE users(

        user_id             INTEGER NOT NULL PRIMARY KEY,
        first_name          VARCHAR,
        last_name           VARCHAR,
        gender              VARCHAR,
        level               VARCHAR
        
);
""")

song_table_create = ("""

CREATE TABLE songs(

        song_id             VARCHAR NOT NULL PRIMARY KEY,
        title               VARCHAR ,
        artist_id           VARCHAR ,
        year                INTEGER ,
        duration            FLOAT
        
);
""")

artist_table_create = ("""

CREATE TABLE artists(

        artist_id           VARCHAR  NOT NULL PRIMARY KEY,
        name                VARCHAR ,
        location            VARCHAR,
        latitude            FLOAT,
        longitude           FLOAT
        
);
""")

time_table_create = ("""

CREATE TABLE time(

        start_time          TIMESTAMP  NOT NULL PRIMARY KEY,
        hour                INTEGER NOT NULL,
        day                 INTEGER NOT NULL,
        week                INTEGER NOT NULL,
        month               INTEGER NOT NULL,
        year                INTEGER NOT NULL,
        weekday             VARCHAR(40) NOT NULL  
        
);
""")

staging_events_copy = (""" 

        COPY staging_events FROM {bucket} 
        CREDENTIALS 'aws_iam_role={role}' 
        region 'us-west-2' 
        FORMAT as JSON {log_json_path} timeformat as 'epochmillisecs'; 
        """).format(bucket=config['S3']['LOG_DATA'], 
                    role=config['IAM_ROLE']['ARN'], 
                    log_json_path=config['S3']['LOG_JSONPATH'])


staging_songs_copy = ("""

        COPY staging_songs FROM {bucket} 
        CREDENTIALS 'aws_iam_role={role}' 
        region 'us-west-2' 
        FORMAT as JSON 'auto'; 
        """).format(bucket=config.get("S3","SONG_DATA"), 
                    role=config.get("IAM_ROLE","ARN"))


# Inserting

songplay_table_insert = ("""

INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)

        SELECT DISTINCT timestamp 'epoch' + e.ts/1000 * interval '1 second' as start_time,
                                 e.userId,
                                 e.level,
                                 s.song_id,
                                 s.artist_id,
                                 e.sessionId,
                                 e.location,
                                 e.userAgent
        FROM staging_events as e
        JOIN staging_songs as s
        ON e.song = s.title
        AND e.artist = s.artist_name
        AND e.length = s.duration
        WHERE e.page='NextSong';
        
""")

user_table_insert = ("""

INSERT INTO users (user_id, first_name, last_name, gender, level)

        SELECT DISTINCT userId as user_id, firstName as first_name, lastName  as last_name, gender, level
        FROM staging_events WHERE page = 'NextSong';
        
""")

song_table_insert = ("""

INSERT INTO songs (song_id, title, artist_id, year, duration)
    
        SELECT DISTINCT song_id, title, artist_id, year,duration 
        FROM staging_songs;

""")

artist_table_insert = ("""

INSERT INTO artists (artist_id, name, location, latitude, longitude)

        SELECT DISTINCT artist_id, artist_name as name, artist_location as location, artist_latitude as latitude, 
        artist_longitud as longitude 
        FROM staging_songs;
      
""")

time_table_insert = ("""

INSERT INTO time (start_time, hour, day, week, month, year, weekday)

        SELECT DISTINCT start_time, 
               EXTRACT(hour from start_time) as hour,
               EXTRACT(day from start_time) as day,
               EXTRACT(week from start_time) as  week,
               EXTRACT(month from start_time) as  month,
               EXTRACT(year from start_time) as  year,
               EXTRACT(weekday from start_time) as  weekday
        FROM songplays;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
