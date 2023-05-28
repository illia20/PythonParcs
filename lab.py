from Pyro4 import expose

class Solver:
    def __init__(self, workers = None, input_file_name = None, output_file_name = None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers

    def solve(self):
        r = self.read_input()
        worker_amount = len(self.workers)
        interval = int(2 * r / worker_amount)
        mapped = []
        for i in range(0, worker_amount):
            mapped.append(self.workers[i].mymap(-r + i * interval, -r + (i + 1) * interval, r))
        result = self.myreduce(mapped)
        self.write_output(result)

    @staticmethod
    @expose
    def mymap(a, b, r):
        result = 0
        for i in range(a, b):
            for j in range(-r, r + 1):
                if Solver.inside_circle(i, j, r):
                    result += 1
        return result

    @staticmethod
    @expose
    def myreduce(mapped):
        output_result = 0
        for x in mapped:
            output_result += int(x.value)
        return output_result + 1

    def read_input(self):
        f = open(self.input_file_name, 'r')
        line = f.readline()
        f.close()
        return int(line)

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        f.write(str(output) + '\n')
        f.close()

    @staticmethod
    @expose
    def inside_circle(x, y, r):
        if (x*x + y*y <= r*r):
            return True
        return False