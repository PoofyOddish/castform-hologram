/****************** WEATHER DATA ******************/
DROP TABLE IF EXISTS weather;

CREATE TABLE weather (
  weather_id INTEGER PRIMARY KEY AUTOINCREMENT,
  category TEXT NOT NULL,
  starttime DATETIME NOT NULL,
  endtime DATETIME NOT NULL,
  daytime BOOLEAN NOT NULL,
  temperature INTEGER NOT NULL,
  forecast TEXT NOT NULL,
  ISACTIVE BOOLEAN NOT NULL
);

/****************** CASTFORM DATA ******************/
DROP TABLE IF EXISTS castform;

CREATE TABLE castform (
  castform_id INTEGER PRIMARY KEY AUTOINCREMENT,
  img TEXT NOT NULL,
  daytime BOOLEAN NOT NULL,
  forecast TEXT NOT NULL
);

INSERT INTO castform (img,daytime,forecast)
VALUES ("castform-normal.png",'False',"Clear"),
    ("castform-sunny.png",'True',"Sunny"),
    ("castform-unsure.png",'True',"Unsure"),
    ("castform-unsure.png",'False',"Unsure"),
    ("castform-rainy.png",'True','Rain'),
    ("castform-rainy.png",'False','Rain')

    ;

  /****************** CASTFORM VIEW ******************/
  DROP VIEW IF EXISTS vw_castform;
  
  CREATE VIEW vw_castform
  as
  select castform.img
    ,castform.forecast
    from castform
    join (
      SELECT daytime,
        CASE
          when forecast like 'Mostly Clear%' then 'Clear'
          when forecast like 'Mostly Sunny%' then 'Sunny'
          when forecast like 'Partly Sunny%' then 'Sunny'
          when forecast like '%Rain Showers' then 'Rain'
          else 'Unsure'
        end as forecast
        from weather
        where ISACTIVE = 1
    ) w 
      on castform.forecast = w.forecast 
        and castform.daytime = w.daytime;