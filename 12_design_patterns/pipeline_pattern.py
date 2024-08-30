class Stage:
    def __init__(self, name):
        self.name = name
    
    def process(self, data):
        raise NotImplementedError("Each Stage must implement the process method")
        

class RemoveSpaces(Stage):
    def __init__(self):
        super().__init__("RemoveSpaces")
        
    def process(self, data):
        return data.replace(" ", "-")
    

class RemoveSpecialChars(Stage):
    def __init__(self, chars_to_remove):
        super().__init__("RemoveSpecialChars")
        self.chars_to_remove = chars_to_remove
        
        
    def process(self, data):
        import re
        pattern = f"[{re.escape(self.chars_to_remove)}]"
        return re.sub(pattern, "", data)
    

class Pipeline:
    def __init__(self, stage_names, chars_to_remove=None):
        self.chars_to_remove = chars_to_remove
        self.stage_names = stage_namesc
        self.stages = self._create_stages()
        
    def _create_stages(self):
        stages = []
        for name in self.stage_names:
            if name == "RemoveSpaces":
                stages.append(RemoveSpaces())
            elif name == "RemoveSpecialChars":
                stages.append(RemoveSpecialChars(self.chars_to_remove))
            else:
                raise ValueError(f"Unnknown Stage name {name}")
        return stages
        
    def run(self, data):
        for stage in self.stages:
            data = stage.process(data)
        
        return data
    
if __name__ == "__main__":
    stage_names = ["RemoveSpaces", "RemoveSpecialChars"]
    chars_to_remove = "@*!&"
    pipeline = Pipeline(stage_names=stage_names, chars_to_remove=chars_to_remove)
    input_data = "This@ is my &input!"
    output_data = pipeline.run(data=input_data)
    
    print(f"Input_data: {input_data}")
    print(f"Output_data: {output_data}")
    
    
    
        