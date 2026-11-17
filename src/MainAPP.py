import wx
from apscheduler.schedulers.blocking import BlockingScheduler


class MainAppliction:
    scheduler = BlockingScheduler()

    def __init__(self, parent):
        super(MainAppliction, self).__init__(parent, title='wx.GridBagSizer', size=(1080, 720))
        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        panel = wx.Panel(self)
        sizer = wx.GridBagSizer(4, 4)
        text = wx.StaticText(panel, label="winrar.exe路径")
        sizer.Add(text, pos=(0, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        self.tc = wx.TextCtrl(panel)
        sizer.Add(self.tc, pos=(1, 0), span=(1, 5), flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=5)

        text1 = wx.StaticText(panel, label="备份文件路径")
        sizer.Add(text1, pos=(2, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        self.tc1 = wx.TextCtrl(panel)
        sizer.Add(self.tc1, pos=(3, 0), span=(1, 5), flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=5)

        text2 = wx.StaticText(panel, label="解压路径")
        sizer.Add(text2, pos=(4, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        self.tc2 = wx.TextCtrl(panel)
        sizer.Add(self.tc2, pos=(5, 0), span=(1, 5), flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=5)

        buttonOk = wx.Button(panel, label="Ok", size=(90, 28))
        buttonOk.Bind(wx.EVT_BUTTON, self.onOk)
        buttonClose = wx.Button(panel, label="Close", size=(90, 28))
        buttonClose.Bind(wx.EVT_BUTTON, self.onClose)
        sizer.Add(buttonOk, pos=(7, 6))
        sizer.Add(buttonClose, pos=(7, 7), flag=wx.RIGHT | wx.BOTTOM, border=5)
        sizer.AddGrowableCol(1)
        # sizer.AddGrowableRow(2)
        panel.SetSizerAndFit(sizer)


