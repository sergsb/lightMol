import base64
import shutil

from lightMol.utils import getSmilesColumn

class VisualizationResult:
    def __init__(self, svg):
        self.svg = svg
    def _repr_html_(self):
        return self.svg
    def _repr_svg_(self):
        return self.svg
    def draw(self,filename):
        with open(filename,'w') as f:
            f.write(self.svg)

    def show(self):
        #Check if feh is installed:
        assert bool(shutil.which("feh")), 'Could not find feh, please install it and retry to use for this function call'
        #Check imagemagick is installed
        assert bool(shutil.which("convert")),'Could not find ImageMagic, please install it and retry to use for this function call'
        import os
        import random
        import string
        randomName = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        filename = "/tmp/temp_{}.svg".format(randomName)
        with open(filename,'w') as f:
            f.write(self.svg)
        os.system('feh --conversion-timeout 1 {}'.format(filename))

    def get(self):
        return self.svg







class LightMolDepictor():
        """
        This is the package for molecular visualization using different backends.
        """
        def _base64Encoder(self,string):
            return base64.b64encode(string.encode('utf-8')).decode('utf-8')

        def _addWebeader(self,string):
            return 'data:image/svg+xml;base64,' + string

        def _rdkitImgFromSmilesToSvg(self,smiles, size=(300, 300)):
            from rdkit import Chem
            from rdkit.Chem.Draw import rdMolDraw2D
            mol = Chem.MolFromSmiles(smiles)
            if mol is None:
                return None
            else:
                drawer = rdMolDraw2D.MolDraw2DSVG(size[0], size[1])
                drawer.DrawMolecule(mol)
                drawer.FinishDrawing()
                svg = drawer.GetDrawingText()
                return self._addWebeader(self._base64Encoder(svg))

        def _openbabelImgFromSmilesToSvg(self, smiles, size=(300, 300)):
            from openbabel import pybel
            mol = pybel.readstring("smi", smiles)
            if mol is None:
                return None
            else:
                mol.draw(show=False)
                return self._addWebeader(self._base64Encoder(mol.write('svg')))

        backends_available = []
        try:
            from rdkit import Chem
            from rdkit.Chem import Draw
            from rdkit.Chem.Draw import rdMolDraw2D
            backends_available.append('rdkit')
        except ImportError:
            pass
        try:
            import pybel
            backends_available.append('openbabel')
        except ImportError:
            pass
        assert len(backends_available) > 0, 'No backend available for depiction, please install rdkit or openbabel'

        def __init__(self,backend='rdkit',web=True):
              self.backend = backend if backend in self.backends_available else self.backends_available[0]
              if self.backend != backend:
                  print('Backend {} is not available, using {} instead'.format(backend,self.backend))

        def __call__(self, *args, **kwargs):
            if kwargs is None: kwargs = {}
            if self.backend == 'rdkit':
                return VisualizationResult(self._rdkitImgFromSmilesToSvg(*args, **kwargs))
            elif self.backend == 'openbabel':
                return VisualizationResult(self._openbabelImgFromSmilesToSvg(*args, **kwargs))

        def process(self, data,*args,**kwargs):
            """
            Multi-tool for processing data.
            :param data: A pandas dataframe with smiles column.
            :return:
            """
            def robust(*args,**kwargs):
                try:
                    return self.__call__(self,*args,**kwargs)
                except Exception as e:
                    print(e)
                    return None

            smilesColumn = getSmilesColumn(data)
            try:
                import pandas as pd
                if isinstance(data, pd.DataFrame):
                    imgs = data[smilesColumn].apply(robust, args=args, kwargs=kwargs)
                    data['img'] = imgs
                    return data
            except ImportError:
                pass
            except Exception as e:
                raise e

#import pandas as pd
#l = LightMolDepictor(backend='rdkit')

