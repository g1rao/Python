import os

class FootBall:
    """ FootBall Game Metrics Analysis """

    def __init__(self, _file):
        self._file = _file
        self.data = self._file_reader(self._file)

    def validate_file(self, _file):
        """ Validates the given input file """
        try:
            if os.path.exists(_file):
                return True
        except Exception as E:
            print(f"File {_file} doesn't exist")
        return False        

    def _file_reader(self, _file):
        """ Reads file and returns data """
        data = []
        if not self.validate_file(self._file):
            return False
        with open(_file) as _file_obj:
            data = _file_obj.readlines()
        return data

    def validate_row(self, data_row):
        """ Validates given team data """
        # check if number of columns
        # column data validation
        if data_row:
            valid_row = []
            for item in data_row.strip().split(","):
                if item.strip() == "":
                    print(f"Invalid row found:\t{data_row}")
                    return False
                valid_row.append(item.strip())
            if len(valid_row) != 7:
                print(f"Invalid row found(Missing columns):\t{data_row}")
                return False
            else:
                return valid_row
        return False

    def _data_analysis(self):
        team_analytics = []
        if not self.data:
            print(f"No data available in the given file {self._file}")
            return None
        for row in self.data[1:]:
            parsed_data = self.validate_row(row)
            fb_metrics = ["Team","Games","Wins","Losses","Draws","Goals For","Goals Against"]
            if parsed_data:
                team_data = dict(zip(fb_metrics,parsed_data)) #{"Team": 'Manchester', "Wins": 33,"GoalDelta": 4 }
                team_data["goal_delta"] = abs(int(team_data["Goals For"]) - int(team_data["Goals Against"])) 
                team_analytics.append(team_data)

        print (team_analytics)
        analyzed_data = sorted(team_analytics, key=lambda _dict: _dict['goal_delta'], reverse= True)
        print("\n\nTeam Name, \t Goals Delta")
        for team_data in analyzed_data:
            print(f"{team_data['Team']}\t\t{team_data['goal_delta']}")

if __name__ == "__main__":
    fb = FootBall("input.txt")
    fb._data_analysis()
