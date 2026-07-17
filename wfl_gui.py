from tkinter import messagebox
import customtkinter as ctk
from pathlib import Path
import threading
import subprocess
import logging as log

log.basicConfig(level=log.INFO,
                filename=Path.joinpath(Path(__file__).parent, "wflgui.log"),
                encoding="utf-8",
                filemode="a",
                format="{asctime} {levelname}: {message}", 
                style="{", 
                datefmt="%Y-%m-%d %H:%M")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("WFL-ASR Refactor Inference GUI")
        self.gui()

    def gui(self):
        self.grid_columnconfigure((0, 1, 2), weight=1)

        # select folder
        #== select folder frame
        selectfolder_frame = ctk.CTkFrame(master=self)
        selectfolder_frame.grid(padx=10, pady=(10, 5), sticky="ew", columnspan=3)
        selectfolder_frame.grid_columnconfigure(0, weight=1)
        selectfolder_frame.grid_columnconfigure(1, weight=0)

        #== select folder label
        selectfolder_label = ctk.CTkLabel(master=selectfolder_frame, text="Select Input Folder")
        selectfolder_label.grid(padx=10, pady=(10, 0), sticky="ew", columnspan=3)

        #== folder path textbox
        self.foldertext = ctk.CTkEntry(master=selectfolder_frame, placeholder_text="folder path here")
        self.foldertext.grid(padx=(10, 5), pady=10, sticky="ew")

        #== browse folder button
        browsefolderbutton = ctk.CTkButton(master=selectfolder_frame, text="Browse Folder", command=self.selectinputfolder)
        browsefolderbutton.grid(row=1, column=2, padx=(5, 10), pady=10, sticky="ew")

        #======================================================

        # model settings
        #== model settings frame
        model_setting_frame = ctk.CTkFrame(master=self)
        model_setting_frame.grid(padx=10, pady=5, sticky="ew", columnspan=3)
        model_setting_frame.grid_columnconfigure((0, 1, 2), weight=1)

        #==== model settings frame label
        model_setting_frame_label = ctk.CTkLabel(master=model_setting_frame, text="Model Settings")
        model_setting_frame_label.grid(padx=10, pady=(10, 0), sticky="ew", columnspan=3)

        #==== model select
        self.readmodel()
        models = []
        configs = []
        self.langids = []
        for m in self.modlist:
            models.append(str(Path(m[0]).name))
        self.modelsv = ctk.StringVar(value="Select Model")
        self.ckptv = ctk.StringVar()

        #====== model frame
        model_frame = ctk.CTkFrame(master=model_setting_frame)
        model_frame.grid(padx=(10, 5), pady=10, sticky="ew")
        model_frame.grid_columnconfigure(0, weight=1)

        #======== model label
        model_label = ctk.CTkLabel(master=model_frame, text="Model")
        model_label.grid(padx=10, pady=(10, 0), sticky="ew")

        #======== model combobox
        self.model_combobox = ctk.CTkComboBox(model_frame, values=models, variable=self.modelsv, state="readonly", command=self.checkcombobox)
        self.model_combobox.grid(padx=10, pady=10, sticky="ew")

        # config select
        self.configsv = ctk.StringVar()

        #== config frame
        config_frame = ctk.CTkFrame(master=model_setting_frame)
        config_frame.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        config_frame.grid_columnconfigure(0, weight=1)

        #==== config label
        config_label = ctk.CTkLabel(master=config_frame, text="Config")
        config_label.grid(padx=10, pady=(10, 0), sticky="ew")

        #==== config combobox
        self.configid_combobox = ctk.CTkComboBox(config_frame, values=configs, variable=self.configsv, state="readonly", command=self.checkcombobox)
        self.configid_combobox.grid(padx=10, pady=10, sticky="ew")

        # language id
        self.langsv = ctk.StringVar()

        #== language id frame
        lang_frame = ctk.CTkFrame(master=model_setting_frame)
        lang_frame.grid(row=1, column=2, padx=(5, 10), pady=5, sticky="ew")
        lang_frame.grid_columnconfigure(0, weight=1)

        #==== language id label
        lang_label = ctk.CTkLabel(master=lang_frame, text="Language ID")
        lang_label.grid(padx=10, pady=(10, 0), sticky="ew")

        #====== language id combobox
        self.lang_combobox = ctk.CTkComboBox(lang_frame, values=self.langids, variable=self.langsv, state="readonly", command=self.checkcombobox)
        self.lang_combobox.grid(padx=10, pady=10, sticky="ew")

        #======================================================

        # silence settings
        sil_setting_frame = ctk.CTkFrame(master=self)
        sil_setting_frame.grid(padx=10, pady=5, sticky="ew", columnspan=3)
        sil_setting_frame.grid_columnconfigure((0, 1, 2), weight=1)

        sil_setting_frame_label = ctk.CTkLabel(master=sil_setting_frame, text="Silence Settings")
        sil_setting_frame_label.grid(padx=10, pady=(10, 0), sticky="ew", columnspan=3)

        #== silence threshold
        #==== silencethreshold frame
        silthreshold_frame = ctk.CTkFrame(master=sil_setting_frame)
        silthreshold_frame.grid(padx=(10, 5), pady=(5, 10), sticky="ew")
        silthreshold_frame.grid_columnconfigure(0, weight=1)

        #====== silence threshold label
        silthreshold_label = ctk.CTkLabel(master=silthreshold_frame, text="Silence Threshold")
        silthreshold_label.grid(padx=10, pady=10, sticky="ew")

        #====== silence threshold value
        self.silthreshdef = ctk.DoubleVar(value=0.005)
        self.silthresh = ctk.DoubleVar(value=0.005)
        self.silbox = ctk.CTkEntry(master=silthreshold_frame, textvariable=self.silthresh, width=50)
        self.silbox.grid()

        #====== silence threshold slider
        self.silslider = ctk.CTkSlider(master=silthreshold_frame, from_=0, to=1, number_of_steps=200, variable=self.silthresh, command=self.slidercall)
        self.silslider.grid(padx=10, pady=10, sticky="ew")

        self.silslider.bind("<Button-3>", self.resetsilslider)

        #== silence phoneme
        self.silphnvar = ctk.StringVar(value="SP")

        #==== silence phoneme frame
        silphn_frame = ctk.CTkFrame(master=sil_setting_frame)
        silphn_frame.grid(row=1, column=1, padx=5, pady=(5, 10), sticky="nsew")
        silphn_frame.grid_columnconfigure(0, weight=1)

        #====== silence phoneme label
        silphn_label = ctk.CTkLabel(master=silphn_frame, text="Silence Phoneme")
        silphn_label.grid(padx=10, pady=10, sticky="ew")

        #====== silence phoneme entry
        silphn_entry = ctk.CTkEntry(master=silphn_frame, placeholder_text="silence phoneme here", textvariable=self.silphnvar, width=50)
        silphn_entry.grid(padx=10, pady=10)

        silphn_entry.bind("<FocusOut>", self.cmdgen_bind)
        silphn_entry.bind("<Return>", self.cmdgen_bind)

        #== silence duration
        #==== silence duration frame
        sildur_frame = ctk.CTkFrame(master=sil_setting_frame)
        sildur_frame.grid(row=1, column=2, padx=(5, 10), pady=(5, 10), sticky="ew")
        sildur_frame.grid_columnconfigure(0, weight=1)

        #====== silence duration label
        sildur_label = ctk.CTkLabel(master=sildur_frame, text="Minimum Silence Duration")
        sildur_label.grid(padx=10, pady=10, sticky="ew")

        #====== silence duration value
        self.minsildurdef = ctk.DoubleVar(value=0.5)
        self.minsildur = ctk.DoubleVar(value=0.5)
        minsilbox = ctk.CTkEntry(master=sildur_frame, textvariable=self.minsildur, width=50)
        minsilbox.grid(row=5)
        
        #====== silence duration slider
        self.minsil_slider = ctk.CTkSlider(master=sildur_frame, from_=0, to=60, number_of_steps=120, variable=self.minsildur, command=self.cmdgen_bind)
        self.minsil_slider.grid(row=6, padx=10, pady=10, sticky="ew")

        self.minsil_slider.bind("<Button-3>", self.resetminsilslider)

        #======================================================

        # additional settings
        #== additional settings frame
        addsetting_frame = ctk.CTkFrame(master=self)
        addsetting_frame.grid(padx=10, pady=5, sticky="ew", columnspan=3)
        addsetting_frame.grid_columnconfigure((0, 1, 2), weight=1)

        #==== additional settings label
        addsetting_label = ctk.CTkLabel(master=addsetting_frame, text="Additional Settings")
        addsetting_label.grid(padx=10, pady=(10, 0), sticky="ew", columnspan=3)

        #== no use offset
        self.nooffset = ["", "--no_use_offset"]
        self.nooffset_var = ctk.StringVar(value=self.nooffset[0])

        #==== no use offset frame
        nooffset_frame = ctk.CTkFrame(master=addsetting_frame)
        nooffset_frame.grid(padx=10, pady=10, sticky="ew", columnspan=3)
        nooffset_frame.grid_columnconfigure((0, 1, 2), weight=1)

        #====== no use offset checkbox
        nooffset_check = ctk.CTkCheckBox(master=nooffset_frame, text="Disable offset head refinement", onvalue=self.nooffset[1], offvalue=self.nooffset[0], variable=self.nooffset_var, command=self.getnooffset)
        nooffset_check.grid(padx=10, pady=10, sticky="ew", columnspan=3)     

        #======================================================

        # generated command
        #== generated command frame
        gencmd_frame = ctk.CTkFrame(master=self)
        gencmd_frame.grid(padx=10, pady=5, sticky="ew", columnspan=3)
        gencmd_frame.grid_columnconfigure((0, 1), weight=1)

        #==== generated command label
        gencmd_label = ctk.CTkLabel(master=gencmd_frame, text="Generated Command")
        gencmd_label.grid(padx=10, pady=(10, 0), sticky="ew", columnspan=2)

        #==== generated command text entry
        self.gencmd_text = ctk.CTkEntry(master=gencmd_frame, placeholder_text="generated command here")
        self.gencmd_text.grid(row=1, padx=10, pady=10, sticky="ew", columnspan=2)

        self.gencmd_text.bind("<FocusOut>", self.commandedit)
        self.gencmd_text.bind("<Return>", self.commandedit)

        #======================================================

        # run inference button
        self.runinf_button = ctk.CTkButton(master=self, text="Run Inference", command=self.runinference)
        self.runinf_button.grid(padx=10, pady=5, sticky="ew", columnspan=3)

        #======================================================

        # command output
        #== command output frame
        cmdout_frame = ctk.CTkFrame(master=self)
        cmdout_frame.grid(padx=10, pady=(5, 10), sticky="ew", columnspan=3)
        cmdout_frame.grid_columnconfigure((0, 1), weight=1)

        #==== command output label
        cmdout_label = ctk.CTkLabel(master=cmdout_frame, text="Command Output")
        cmdout_label.grid(padx=10, pady=(10, 0), sticky="ew", columnspan=3)

        #==== command output textbox
        self.cmdout_text = ctk.CTkTextbox(master=cmdout_frame)
        self.cmdout_text.grid(padx=10, pady=(10, 5), sticky="ew", columnspan=3)

        #==== progressbar
        self.inference_progress = ctk.CTkProgressBar(master=cmdout_frame, orientation="horizontal")
        self.inference_progress.grid(padx=(10, 0), pady=(0, 5), sticky="ew", columnspan=2)
        self.inference_progress.set(0)

        #==== progressbar tracker
        self.inference_progress_label = ctk.CTkLabel(master=cmdout_frame, text="0/?", width=70)
        self.inference_progress_label.grid(row=2, column=2, padx=10, pady=(0, 5))

    def selectinputfolder(self):
        self.wavcount = 0
        self.inputfolder = ctk.filedialog.askdirectory()
        self.foldertext.set(self.inputfolder)
        log.info(f"Selected input folder: {self.inputfolder}")
        for w in Path(self.inputfolder).iterdir():
            if w.suffix == ".wav":
                self.wavcount += 1
        self.cmdgen()

    def readmodel(self):
        self.parent = Path(__file__).resolve().parent.parent
        self.allmodels_path = Path(self.parent, "models")

        model_paths = []

        for m in self.allmodels_path.iterdir():
            if m.is_dir():
                model_paths.append(str(m))

        self.modlist = []

        for mp in model_paths:
            each = []
            each.append(mp)
            ckpt = []
            cnfg = []
            lngs = []
            for f in Path(mp).iterdir():
                if f.suffix == ".ckpt":
                    ckpt.append(str(Path(f).name))
                elif f.suffix == ".pt":
                    ckpt.append(str(Path(f).name))
                elif f.suffix == ".yaml":
                    cnfg.append(str(Path(f).name))
            with open(Path(mp, "langs.txt"), "r") as f:
                for line in f:
                    langclean = line.rstrip()
                    langsplit = langclean.split(",")
                    lngs.append(f"{langsplit[1]}: {langsplit[0]}")
            each.append(ckpt)
            each.append(cnfg)
            each.append(lngs)
            self.modlist.append(each)

    def checkcombobox(self, e):
        self.readmodel()
        model = self.modlist

        m = self.model_combobox.cget("values")

        for idx, item in enumerate(m):
            if self.modelsv.get() == m[idx]:
                self.configid_combobox.configure(values=model[idx][2])
                self.ckptv.set(model[idx][1][0])
                if self.configsv.get() not in model[idx][2]:
                    self.configsv.set(model[idx][2][0])
                self.lang_combobox.configure(values=model[idx][3])
                if self.langsv.get() not in model[idx][3]:
                    self.langsv.set(model[idx][3][0])
            else: 
                pass
        self.cmdgen()

    def slidercall(self, value):
        rounded = ctk.DoubleVar(value=float(f"{value:.3f}"))
        self.silthresh.set(rounded.get())
        self.cmdgen()

    def cmdgen_bind(self, event):
        self.cmdgen()

    def cmdgen(self):
        self.readmodel()
        checkpoint = self.ckptv.get()
        curmodel = self.modelsv.get()
        curconfig = self.configsv.get()
        curlang = self.langsv.get()
        configpath = Path(self.allmodels_path, curmodel, curconfig)
        checkpointpath = Path(self.allmodels_path, curmodel, checkpoint)
        langid = curlang.split(":")[0]
        inputpath = Path(self.foldertext.get())

        silphn = self.silphnvar.get()
        silthresh = self.silbox.get()
        minsil = self.minsil_slider.get()
        offset = self.nooffset_var.get()

        if curmodel != "Select Model":
            log.info(f"Selected model:    {curmodel}")
            log.info(f"Selected config:   {curconfig}")
            log.info(f"Selected language: {curlang}")

        cmd = [
               f"conda activate wfl &&",
               f"python \"{self.parent}\infer.py\"",
               f"-i \"{inputpath}\"", 
               f"-ckpt \"{checkpointpath}\"", 
               f"-c \"{configpath}\"", 
               f"-l {langid}"
               ]

        if silphn != "SP":
            cmd.append(f"--silence-phoneme {silphn}")
        if silthresh != "0.005":
            cmd.append(f"--silence-threshold {silthresh}")
        if minsil != 0.5:
            cmd.append(f"--min-silence-duration {minsil}")
        if offset == "--no_use_offset":
            cmd.append("--no_use_offset")

        checkcmdempty = "Select Model"
        if curmodel == checkcmdempty or curconfig == checkcmdempty:
            cmd = None

        try:
            self.rescmd = " ".join(cmd)
            if "-i \".\"" not in self.rescmd:
                self.gencmd_text.set(self.rescmd)
            else: return
            log.info(f"Generated command: {self.rescmd}")
        except:
            log.info("No model selected, command not generated")

    def commandedit(self, event):
        self.gencmd_text.set(self.gencmd_text.get())

    def resetsilslider(self, event):
        if self.silthresh.get() != self.silthreshdef.get():
            self.silthresh.set(value=self.silthreshdef.get())
            log.info(f"Silence Threshold set to default: {self.silthresh.get()}")
        elif self.silthresh.get() == self.silthreshdef.get():
            log.info("Silence Threshold is already default")
        else: pass
        self.cmdgen()

    def resetminsilslider(self, event):
        if self.minsildur.get() != self.minsildurdef.get():
            self.minsildur.set(value=self.minsildurdef.get())
            log.info(f"Minimum Silence set to default: {self.minsildur.get()}")
        elif self.minsildur.get() == self.minsildurdef.get(): 
            log.info("Minimum Silence is already default")
        else: pass
        self.cmdgen()

    def getnooffset(self):
        offsethead = ""
        if self.nooffset_var.get() == self.nooffset[0]:
            offsethead = "off"
        elif self.nooffset_var.get() == self.nooffset[1]:
            offsethead = "on"
        log.info(f"Disable offset head refinement: {offsethead}")
        self.cmdgen()

    def runinference(self):
        log.info("Run Inference button pressed")
        self.inference_progress.set(0)
        cmd = self.gencmd_text.get()
        if not cmd:
            messagebox.showwarning("Warning", "No command has been generated yet. Please configure the inference settings.")
            return
        
        self.runinf_button.configure(state="disabled", text="Running Inference...")

        self.cmdout_text.delete(0.0, "end")

        self.progcount = 0
        self.inference_progress_label.configure(text=f"{self.progcount}/{self.wavcount}")

        def stream_output():
            self.cmdout_text.insert("end", "Starting Inference..." + "\n")
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
            for line in proc.stdout:
                self.cmdout_text.insert("end", line + "\n")
                self.cmdout_text.see("end")
                if "Saved ->" in line:
                    self.progcount += 1
                    self.inference_progress.set(self.inference_progress.get() + (1 / self.wavcount))
                    self.inference_progress_label.configure(text=f"{self.progcount}/{self.wavcount}")
            proc.stdout.close()
            proc.wait()

            self.cmdout_text.insert("end", "Finished generating labels!" + "\n")

            self.runinf_button.configure(state="normal", text="Run Inference")

        threading.Thread(target=stream_output, daemon=True).start()

if __name__ == "__main__":
    app = App()
    app.minsize(500, 700)
    app.resizable(width=True, height=False)
    app.mainloop()