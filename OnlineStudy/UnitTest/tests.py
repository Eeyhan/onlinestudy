import matplotlib.pyplot as plt
import base64
from io import BytesIO
from django.shortcuts import render


# def test(request):
#     # fig = plt.figure()
#     plt.plot([1, 2, 3, 4], [10, 20, 25, 30], color='lightblue', linewidth=3)
#     plt.xlim(0.5, 4.5)
#     buffer = BytesIO()
#     plt.savefig(buffer)
#     plot_data = buffer.getvalue()
#     imb = base64.b64encode(plot_data)  # 对plot_data进行编码
#     ims = imb.decode()
#     imd = "data:image/png;base64," + ims
#     return render(request, "test.html", {"img": imd})

def matlab():
    age = [5, 10, 15, 20, 25, 30]
    height = [25, 45, 65, 75, 75, 75]
    plt.plot(age, height)
    plt.title('Age vs Height')
    plt.xlabel('age')
    plt.ylabel('Height')
    plt.show()

matlab()
