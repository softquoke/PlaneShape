from tkinter import Tk, Canvas, Frame, BOTH
import json
import pprint


class PlaneShape(Frame):    

    def __init__(self, points_figure, root_size, range_size):
        super().__init__()
        self.root_size = root_size
        self.points_figure = points_figure
        self.range_size = range_size
        self.basic_lines = []
        self.connecting_lines = []


    def initUI(self):
        print('//initUI()')
        self.master.title("Рисуем линии")
        self.pack(fill=BOTH, expand=1)
        self.update_idletasks()
        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=1)

    def draw_figure(self):
        print('\n//draw_figure()')
        for i in range(0, len(self.basic_lines)):    
            self.draw_line(self.basic_lines[i]["coordinates"], width=2)     

    def draw_connecting_lines(self):
        print("\n//draw_connecting_lines()")
        for i in range(0, len(self.connecting_lines)):
            self.draw_line(self.connecting_lines[i]["coordinates"], width=1, fill="#faa7c3")
 
    def draw_line(self, coodinates:dict, width:int = 1, fill:str = "#000"):
        """
        В данную функцию передается 2 массива заложенных в массив coordinates
        каждый из массивов это координаты х, y начальной и конечной точки
        """
        
        print("//draw_line() -", coodinates)
        self.canvas.create_line(
            coodinates[0][0], 
            self.root_size[1] - (coodinates[0][1] + self.range_size),
            coodinates[1][0],
            self.root_size[1] - (coodinates[1][1] + self.range_size),
            width=width,
            fill=fill
        )

    def set_equation(self, points_figure: dict) -> dict:
        #уравнение прямой

        try:
            k = (points_figure[1][1] - points_figure[0][1]) / (points_figure[1][0] - points_figure[0][0])
            b = points_figure[0][1] - ((points_figure[1][1] - points_figure[0][1]) / (points_figure[1][0] - points_figure[0][0]) * points_figure[0][0])
            answer = {
                "relation": "y from x",
                "coordinates": [points_figure[0], points_figure[1]], 
                "k": round(k, 3), 
                "b": round(b, 3)
            }  
            return answer
        except ZeroDivisionError:
            answer = {
                "relation": "x from y",
                "x": points_figure[0][0],
                "coordinates": [points_figure[0], points_figure[1]]
            }   
        
            return answer
        
        
    
    def formation_of_basic_lines(self):
        print("\n//formation_of_basic_lines()")
        for i in range(0, len(self.points_figure) - 1):
            self.basic_lines.append(
                self.set_equation([self.points_figure[i],
                                   self.points_figure[i + 1]])
            )
        pprint.pprint(self.basic_lines)    

    #TODO надо правильно сравнить линии
    def selection_of_connecting_lines(self):        
        print('\n//selection_of_connecting_lines()')
        flag = True        
        for i in range(0, len(self.points_figure) - 2):
            for j in range(i + 2, len(self.points_figure) - 1):
                equation = self.set_equation([self.points_figure[i], self.points_figure[j]])
                print("\nequation ", equation)
                
                for basic_line in self.basic_lines:
                    print("basic line ", basic_line)
                    if sum([sum(item) for item in equation["coordinates"]]) == sum([sum(item) for item in basic_line["coordinates"]]):
                        if (equation["relation"] == basic_line["relation"]) and (equation["relation"] == "y from x"):
                            if (abs(equation["k"]) == abs(basic_line["k"])) and (equation["b"] == basic_line["b"]):
                                print("\nALARM, the coincidence of the equation with:")
                                pprint.pprint(basic_line)
                                flag = False
                                print('-'*50)
                                break
                        elif (equation["relation"] == basic_line["relation"]) and (equation["relation"] == "x from y"):
                            if (equation["x"] == basic_line["x"]):
                                print("\nALARM, the coincidence of the equation with:")
                                pprint.pprint(basic_line)
                                flag = False
                                print('-'*50)
                                break
                if flag:
                    print("\nGOOD, append is:")
                    pprint.pprint(equation)
                    self.connecting_lines.append(equation)
                    flag = True
                    print('-'*50)
                else:
                    flag = True
        
        print(f"\nCount connecting lines - {len(self.connecting_lines)}:")
        pprint.pprint(self.connecting_lines)


def main():

    with open("test1.json", "r") as file:
        data = json.load(file)

    range_size = 50
    
    """
    0 - трапеция
    1 - квадрат
    2 - сердечко
    3 - перевернутая буква П
    """
    points_figure = [[coordinate[0] * range_size, 
                coordinate[1] * range_size] 
                for coordinate in data["points_figures"][3]] # индекс - номер фигуры из test1.json
    root = Tk()
    
    height = 500
    width = 500
    root.geometry(f'{width}x{height}+{int(root.winfo_screenwidth()/2)-int(width/2)}+{int(root.winfo_screenheight()/2)-int(height/2)}')
    root.attributes("-alpha", 0.9)

      
    complex_figure = PlaneShape(points_figure, (width, height), range_size)

    complex_figure.initUI()    

    complex_figure.formation_of_basic_lines()
    complex_figure.selection_of_connecting_lines()
    complex_figure.draw_figure()
    complex_figure.draw_connecting_lines()


    # print("\nbasic lines:")
    # pprint.pprint(complex_figure.basic_lines)
    # print("\nconnecting lines")
    # pprint.pprint(complex_figure.connecting_lines)

    #TODO
    # complex_figure.draw_line(complex_figure.basic_lines[-1]["coordinates"], width=2)
    # complex_figure.draw_line(complex_figure.connecting_lines[2]["coordinates"], width=1, fill="red")
    # print("\nbasic line:")
    # pprint.pprint(complex_figure.basic_lines[4])
    # print("\nconnecting line:")
    # pprint.pprint(complex_figure.connecting_lines[2])

    root.mainloop()


if __name__ == "__main__":
    main()
