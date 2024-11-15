
import matplotlib.pyplot as plt
import numpy as np
from mplcursors import cursor
from matplotlib.widgets import CheckButtons
from matplotlib.ticker import MaxNLocator
from matplotlib.transforms import Bbox

import os
os.system('mode con: cols=170 lines=30')

class Constants:
    def __init__(self, dt):
        self.Q = 33.5
        self.V_p = 338
        self.CL_l = 0.583
    
        self.V_c = 173
        self.k_a = 2.41
        self.k_23 = self.Q / self.V_c
        self.k_32 = self.Q / self.V_p
        self.k_20 = self.CL_l / self.V_c
        self.V_max = 5.91
        self.K_m = 0.957
        self.V_ss = 511
        
        self.DHT_ss = 488
        self.k_out = 0.393
        self.FAR_2 = 0.827
        self.k_1 = 0.0153
        self.k_2 = 0.00871
        self.ko_1 = 0.000594
        self.ko_2 = 0.0357
        
        self.dt = dt
        self.dt2 = 0.5 * dt ** 2

class Compartments:
    def __init__(self, const):
        self.A_1 = 0
        self.A_2 = 0
        self.A_3 = 0
        self.A_4 = 0
        
        self.DHT = const.DHT_ss
        self.DHTp = 0
        self.scalpDHTp = 0
        
        self.S5AR1 = 1
        self.S5AR2 = 1
        
    def administer(self, mg):
        self.A_1 += mg * 1000
    
        
class SimulationData:
    def __init__(self):
        self.ySerumDut = []
        self.ySerumDHTSup = []
        self.yScalpDHTSup = []
        self.numSamples = 0
        self.totalSimTime = 0
        
class Schedule:
    def __init__(self, text):
        self.dosingPattern = []
        self.totalRunTime = 0
        text = ''.join(text.split())
        splitByComma = []
        bracketDepth = 0
        startI = 0
        for i in range(len(text)):
            ch = text[i]
            if ch == '[':
                bracketDepth += 1
            elif ch == ']':
                bracketDepth -= 1
            elif ch == ',' and bracketDepth == 0:
                if i > startI:
                    splitByComma.append(text[startI:i])
                startI = i + 1
        if startI < len(text):
            splitByComma.append(text[startI:])
                    
        if bracketDepth != 0:
            return
        
        dosingPattern = []
        daysOfWeek = ['Su', 'M', 'Tu', 'W', 'Th', 'F', 'Sa']
        for commaSplit in splitByComma:
            if commaSplit[0] != '[':
                return
            endI = 0
            try:
                endI = commaSplit.index(']')
            except:
                return
            intervalStr = commaSplit[1:endI]
                
            totalTime = -1
            if len(commaSplit) > endI + 2 and commaSplit[endI + 1] == 'x':
                totalTime = self.parseTimeStringToHours(commaSplit[endI + 2:])
                if totalTime == -1:
                    return
            
            if len(intervalStr) == 0:
                return
                
            intervalStrs = list(filter(None, intervalStr.split(',')))
            
            intervalsList = []
            if len(intervalStrs) % 2 != 0:
                return
            
            if len(intervalStrs) == 2 and any(x in intervalStrs[1] for x in daysOfWeek) and not any(ch.isdigit() for ch in intervalStrs[1]):
                try:
                    dose = float(intervalStrs[0])
                except:
                    return
                
                week = [dow in intervalStrs[1] for dow in daysOfWeek]
                index = (week.index(True) + 1) % 7
                week = week[index:] + week[:index]
                wait = 0
                for i in range(7):
                    wait += 24
                    if week[i]:
                        intervalsList.append((dose, wait))
                        wait = 0
            else:
                for i in range(len(intervalStrs) // 2):
                    j = i * 2
                    dose = 0
                    try:
                        dose = float(intervalStrs[j])
                    except:
                        return
                    timeInterval = self.parseTimeStringToHours(intervalStrs[j + 1])
                    if timeInterval == -1:
                        return
                    intervalsList.append((dose, timeInterval))
            
            
            time = 0
            for i in range(len(intervalsList)):
                time += intervalsList[i][1]
            if totalTime == -1:
                totalTime = time
            
            dosingPattern.append((intervalsList, time, totalTime))
            self.totalRunTime += totalTime
        
        self.dosingPattern = dosingPattern
                
                
    def parseTimeStringToHours(self, string):
        endI = len(string)
        for i in range(len(string)):
            ch = string[i]
            if not (ch.isdigit() or ch == '.'):
                endI = i
                break
        number = 0
        try:
            number = float(string[:endI])
        except:
            return -1
                
        unit = string[endI:]
        if unit == 'd' or unit == '':
            return number * 24
        elif unit == 'w':
            return number * 7 * 24
        elif unit == 'mo':
            return number * 30 * 24
        elif unit == 'y':
            return number * 365 * 24
        elif unit == 'h':
            return number
        else:
            return -1
            
    def indices(self, time):
        if time < 0:
            return None
    
        index1 = 0
        startTime1 = 0
        for i in range(len(self.dosingPattern)):
            totalTime = self.dosingPattern[i][2]
            if time < startTime1 + totalTime:
                break
            index1 += 1
            startTime1 += totalTime
            
        if index1 == len(self.dosingPattern):
            return None
            
        offsetTime = (time - startTime1) % self.dosingPattern[index1][1]
        offsetIndex = int((time - startTime1) / self.dosingPattern[index1][1]) * len(self.dosingPattern[index1][0])
        
        index2 = 0
        startTime2 = 0
        for i in range(len(self.dosingPattern[index1][0])):
            wait = self.dosingPattern[index1][0][i][1]
            if offsetTime < startTime2 + wait:
                break
            index2 += 1
            startTime2 += wait
            
        if index2 == len(self.dosingPattern[index1][0]):
            index2 = 0
            
        return index1, offsetIndex + index2
        
    def doseAt(self, indices):
        if indices == None:
            return 0
        intervals = self.dosingPattern[indices[0]][0]
        interval = intervals[indices[1] % len(intervals)]
        return interval[0]
        
def predictNextCompartmentValues(comp, const, useSecondOrder):
    N = 1
    dt = const.dt
    dt2 = const.dt2

    dS5AR1 = const.k_1 - const.k_1 * comp.S5AR1 - const.ko_1 * comp.A_4 * comp.S5AR1
    dS5AR2 = const.k_2 - const.k_2 * comp.S5AR2 - const.ko_2 * comp.A_4 * comp.S5AR2
    if not (abs(dS5AR1) < comp.S5AR1 * 100 and abs(dS5AR2) < comp.S5AR2 * 100):
        N = 10
        dt /= N
        dt2 /= N * N
        
    A_1 = comp.A_1
    A_2 = comp.A_2
    A_3 = comp.A_3
    A_4 = comp.A_4
    DHT = comp.DHT
    S5AR1 = comp.S5AR1
    S5AR2 = comp.S5AR2
    
    k23k20 = const.k_23 + const.k_20
    for i in range(N):
        vckma2 = const.V_c * const.K_m + A_2
    
        dA_1 = -const.k_a * A_1
        dA_2 = const.k_a * A_1 - k23k20 * A_2 + const.k_32 * A_3 - const.V_max * A_2 / vckma2
        dA_3 = const.k_23 * A_2 - const.k_32 * A_3
        dA_4 = dA_2 / const.V_c
        dDHT = const.k_out * const.DHT_ss * const.FAR_2 * S5AR2 + const.k_out * const.DHT_ss * (1 - const.FAR_2) * S5AR1 - const.k_out * DHT
        dS5AR1 = const.k_1 - const.k_1 * S5AR1 - const.ko_1 * A_4 * S5AR1
        dS5AR2 = const.k_2 - const.k_2 * S5AR2 - const.ko_2 * A_4 * S5AR2
        
        d2A_1 = -const.k_a * dA_1
        d2A_2 = const.k_a * dA_1 - k23k20 * dA_2 + const.k_32 * dA_3 - const.V_max * (vckma2 * dA_2 - A_2 * dA_2) / (vckma2 ** 2)
        d2A_3 = const.k_23 * dA_2 - const.k_32 * dA_3
        d2A_4 = d2A_2 / const.V_c
        d2DHT = const.k_out * const.DHT_ss * const.FAR_2 * dS5AR2 + const.k_out * const.DHT_ss * (1 - const.FAR_2) * dS5AR1 - const.k_out * dDHT
        d2S5AR1 = -const.k_1 * dS5AR1 - const.ko_1 * (A_4 * dS5AR1 + dA_4 * S5AR1)
        d2S5AR2 = -const.k_2 * dS5AR2 - const.ko_2 * (A_4 * dS5AR2 + dA_4 * S5AR2)
        
        A_1 += dA_1 * dt
        A_2 += dA_2 * dt
        A_3 += dA_3 * dt
        A_4 += dA_4 * dt
        DHT += dDHT * dt
        S5AR1 += dS5AR1 * dt
        S5AR2 += dS5AR2 * dt
        
        if useSecondOrder:
            A_1 += d2A_1 * dt2
            A_2 += d2A_2 * dt2
            A_3 += d2A_3 * dt2
            A_4 += d2A_4 * dt2
            DHT += d2DHT * dt2
            S5AR1 += d2S5AR1 * dt2
            S5AR2 += d2S5AR2 * dt2
            
    comp.A_1 = A_1
    comp.A_2 = A_2
    comp.A_3 = A_3
    comp.A_4 = A_4
    comp.DHT = DHT
    comp.S5AR1 = S5AR1
    comp.S5AR2 = S5AR2
    
    comp.DHTp = 100 * (1 - comp.DHT / const.DHT_ss)
    comp.scalpDHTp = 100 * (1 - scalpDHTReduction(comp))
        
def scalpDHTReduction(comp):
    c = comp.A_3
    return 0.358 * (1 - c / (68.515 + c)) + 0.642 * (1 - c / (27397.306 + c))
    
def simulate(dt, schedule, resTime):   
    const = Constants(dt)
    comp = Compartments(const)
    
    numSteps = int(schedule.totalRunTime / dt)
    time = 0
    sampleTime = resTime
    indices = None
    data = SimulationData()
    for i in range(numSteps):
        newIndices = schedule.indices(time)
        if newIndices != indices:
            comp.administer(schedule.doseAt(newIndices))
        indices = newIndices
        if time > schedule.totalRunTime:
            break
        
        while sampleTime >= resTime:
            sampleTime -= resTime
            data.ySerumDut.append(comp.A_4)
            data.ySerumDHTSup.append(comp.DHTp)
            data.yScalpDHTSup.append(comp.scalpDHTp)
            
        predictNextCompartmentValues(comp, const, True)
        time += dt
        sampleTime += dt
        
    data.numSamples = len(data.ySerumDut)
    data.totalSimTime = schedule.totalRunTime
    
    return data

    
while True:
    print('Enter a dosing schedule. Dosing schedule format examples:\n')
    print('\t1)  [0.5, 1d] x 90d = 0.5 mg daily for 90 days.\n')
    print('\t2)  [1, 2d] x 2mo = 1 mg every other day for 2 months.\n')
    print('\t3)  [0.5, 3d, 1, 2d] x 16w = 0.5 mg, wait 3 days, 1 mg, wait 2 days, repeat for 16 weeks.\n')
    print('\t4)  [2.5, 1w] x 0.5y, [0.5, 1d] x 0.5y = 2.5 mg per week for half a year, then 0.5 mg per day for half a year.\n')
    print('\t5)  [0.5, MWF] x 45d = 0.5 mg on Monday Wednesday Friday for 45 days.\n')
    print('\t6)  [1, SaSuTuTh] x 6mo = 1 mg on Saturday Sunday Tuesday Thursday for 6 months.\n')
    print('\t7)  [0.5, 1d] x 1mo, [1, 1d] x 1mo, [1.5, 1d] x 1mo, [2, 1d] x 1mo = Increasing daily dose by 0.5 mg each month.\n')
    
    print('Make sure to specify time units; default unit is days.\n')
    print('Enter \'q\' to quit.\n')
    inp = input('Your dosing schedule: ')
    if ''.join(inp.lower().split()) == 'q':
        break
    schedule = Schedule(inp)
    if len(schedule.dosingPattern) == 0:
        print('Not valid dosing schedule syntax. Press enter to try again.')
        input()
        print()
        continue
    
    simData = simulate(0.01, schedule, 0.01)
        
    x = np.linspace(0, simData.totalSimTime / 24, simData.numSamples)
    ySerumDut = np.array(simData.ySerumDut)
    ySerumDHTSup = np.array(simData.ySerumDHTSup)
    yScalpDHTSup = np.array(simData.yScalpDHTSup)

    fig = plt.figure() 
    ax1 = fig.add_subplot()
    fig.canvas.manager.set_window_title('Gisleskog et al. Dutasteride Pharmacokinetics/Pharmacodynamics Modeling (Fuzzy\'s Implementation)')
    ax2 = ax1.twinx()
    ax3 = ax2.inset_axes([0.0, 0.9, 0.3, 0.1])
    ax3.set_facecolor('white')
        
    serumDutLine, = ax1.plot(x, ySerumDut, color='red', label='Serum Dutasteride (ng/mL)')
    serumDHTSupLine, = ax2.plot(x, ySerumDHTSup, color='green', label='Serum DHT Suppression (%)')
    scalpDHTSupLine, = ax2.plot(x, yScalpDHTSup, color='blue', label='Scalp DHT Suppression (%)')

    scalpDHTThresholdLine = ax2.plot(np.array([0, simData.totalSimTime / 24]), np.array([32, 32]), ':', color='blue', label='Minimum Scalp DHT Reduction (%)\nRequired for Efficacy ≥ Finasteride')


    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_color(serumDutLine.get_color())
    ax1.tick_params(axis='y', colors=serumDutLine.get_color())
    ax1.set_xlabel('Time (days)')
    ax1.set_ylabel(serumDutLine.get_label())
    ax1.tick_params(axis='y', colors=serumDutLine.get_color())
    ax1.yaxis.label.set_color('red')
    ax1.grid(axis='x')

    ax2.spines['left'].set_visible(False)
    ax2.invert_yaxis()
    ax2.yaxis.set_major_locator(MaxNLocator(nbins=10))
    ax2.set_ylabel('DHT Suppression (%)')

    lines = [serumDutLine, serumDHTSupLine, scalpDHTSupLine]
    linesDict = { line.get_label() : line for line in lines }
    lineLabels = [line.get_label() for line in lines]
    lineColors = [line.get_color() for line in lines]
    check = CheckButtons(ax=ax3, labels=lineLabels, actives=[True] * len(lines), label_props={'color': lineColors}, frame_props={'edgecolor': lineColors}, check_props={'facecolor': lineColors})
    for label in check.labels:
        label.set_fontsize(12 / fig.dpi * 72)
        label.set_fontname('DejaVu Sans')

    def on_xlims_change(event):
        bbox = ax1.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        width = bbox.width * fig.dpi

        x1, x2 = tuple(map(float, event.get_xlim()))
        res = int(width)
        ratio = simData.numSamples / simData.totalSimTime
        x1Sample = x1 * 24 * ratio
        x2Sample = x2 * 24 * ratio
        step = (x2Sample - x1Sample) / res
        dummyValues = 1
        dummyValuesIncluded = max(0, min(int(-x1 * res / (x2 - x1)), dummyValues))

        def sampleY(yData):
            ret = []
            for i in range(res):
                ix = int(x1Sample + i * step)
                if ix < -dummyValuesIncluded * step or ix >= len(yData):
                    ret.append(None)
                elif ix < 0:
                    ret.append(0)
                else:
                    ret.append(yData[ix])
            return np.array(ret)
        
        newX = np.linspace(x1, x2, res)
        
        serumDutLine.set_data(newX, sampleY(simData.ySerumDut))
        serumDHTSupLine.set_data(newX, sampleY(simData.ySerumDHTSup))
        scalpDHTSupLine.set_data(newX, sampleY(simData.yScalpDHTSup))
        
        check.ax.set_position([0.0, 0.9, res * 0.01, 0.1])

    ax1.callbacks.connect('xlim_changed', on_xlims_change)

    def on_resize(event):
        ax1.set_xlim(ax1.get_xlim())
        widthi, heighti = fig.get_size_inches()
        dpi = fig.get_dpi()
        width, height = dpi * widthi, dpi * heighti
        def locator(ax, _):
            bbox = ax.get_position()
            return Bbox.from_bounds(bbox.x0, bbox.y0 + bbox.height - 80 / height, 270 / width, 80 / height)
        ax3.set_axes_locator(locator)

    fig.canvas.mpl_connect('resize_event', on_resize)

    ax1.set_xlim(ax1.get_xlim())
    ax1.set_ylim(0, ax1.get_ylim()[1])
    ax2.set_ylim(100, 0)

    def onCheckClicked(label):
        line = linesDict[label]
        line.set_visible(not line.get_visible())
        line.figure.canvas.draw_idle()
        
    check.on_clicked(onCheckClicked)

    def on_close(event):
        ax1.clear()
        ax2.clear()
        ax3.clear()
        fig.clear()
        plt.close(fig)
        
    fig.canvas.mpl_connect('close_event', on_close)
    
    cur = cursor(hover=True)
    @cur.connect("add")
    def _(sel):
        sel.annotation.get_bbox_patch().set(fc="white", alpha=1)
        sel.annotation.arrow_patch.set(arrowstyle="simple", fc="white", alpha=1)

    plt.tight_layout()
    plt.show()
    
    