import numpy as np
from skimage import io
from llsmvis.globals import *
import copy
import os

class WBDeconv:
# this class is developed from the Matlab package associated with the following publication:
# Guo M, Li Y, Su Y, Lambert T, Dalle Nogare D, Moyle MW, Duncan LH, Ikegami R, Santella A, Rey-Suarez I,
# Green D. Accelerating iterative deconvolution and multiview fusion by orders of magnitude. BioRxiv. 2019 Jan 1:647370.
#
# The matlab code package was kindly provided by the authors.
#
# [change to the journal after the manuscript is publisehd online...]
#
# notes for future polish:
# at some point need to make all attributes static, no more no less in future development.. [figure that out later].
#
    def __init__(self, p):
        self.classname = 'WBDeconv'
        self.p = p  # p is the parser for the dataset.
        self.alpha = 0.001  # 0.0001 ~ 0.001 small value used in Wiener filter.
        self.beta = 1  # 0.001 ~ 0.01, resolution cutoff gain, used in Butterworth filter
        self.n = 10  # 4 ~ 15; order of the Butterworth filter
        self.iRes = [0, 0, 0]  # input resolution limit in 3 dimensions in terms of pixels.
        self.resFlag = 1  # 0: use PSF_fp FWHM/root(2) as resolution limit
                          # 1: use PSF_fp FWHM as resolution limit
                          # 2: use input values (iRes) as resolution limit
        self.verboseFlag = VERBOSE # global VERBOSE switch.
        self.bp_type = 'Wiener-Butterworth'  # set default to be Wiener Butterworth back projector.
        self.itN = 1  # iteration number, default is 1, for WBDeconvolution
        self.small_value = 0.1

        # define full path to a raw LLSM tiff stack, without deskew.
        self.raw_stack_path = ''

        # use this as testing default value, change later.
        self.deskewed_path = '/Users/yi10/Desktop/Research/LDRD_LLSM_rendering/openvisustools/demo_data/Demo_claires/Stack_0.tif'

        # define full path to a tiff stack that contains a centered PSF stack.
        self.psf_path = '/Users/yi10/Desktop/Research/LDRD_LLSM_rendering/openvisustools/demo_data/Demo_claires/psf2.tif'

        # get a place holder for a 3D observation stack (as opposed to PSF stack).
        self.current_stack = np.float32(io.imread(self.deskewed_path))
        self.fp = np.nan  # this will be a ForwardProjector object
        self.bp = np.nan  # this will be a BackwardProjector object

    class ForwardProjector:
        def __init__(self, psf_path):
            # initialization shall involve no data loading nor calculations.
            self.psf_path = psf_path
            self.psf_ori = np.nan
            self.psf = np.nan
            self.otf = np.nan
            self.psf_ori_flipped = np.nan
            self.otf_ori_flipped = np.nan
            self.otf_ori_flipped_norm = np.nan
            self.otf_ori_flipped_abs_norm = np.nan

            # fwhm of the psf
            self.FWHMx = np.nan
            self.FWHMy = np.nan
            self.FWHMz = np.nan
            #
            # size of the psf ndarray
            self.Sx = np.nan
            self.Sy = np.nan
            self.Sz = np.nan
            #
            # absolute center of the psf ndarray
            self.Scx = np.nan
            self.Scy = np.nan
            self.Scz = np.nan
            #
            # rounded center of the psf ndarray
            self.Sox = np.nan
            self.Soy = np.nan
            self.Soz = np.nan

        def get_ready(self, fwhm_PSF):
            # load raw PSF stack
            psfin = np.float32(io.imread(self.psf_path))
            psfin = psfin / sum(psfin.ravel())
            self.psf_ori = psfin
            self.psf_ori_flipped = np.flip(self.psf_ori)
            t=np.fft.ifftshift(self.psf_ori_flipped)
            self.otf_ori_flipped=np.fft.fftn(t)  # do this separately seems to be slightly faster...
            otf_ori_flipped_abs = np.fft.fftshift(abs(self.otf_ori_flipped))
            otfmax = [np.max(otf_ori_flipped_abs.ravel())]
            M = otfmax[0]
            self.otf_ori_flipped_abs_norm = otf_ori_flipped_abs / M
            self.otf_ori_flipped_norm = self.otf_ori_flipped / M  # Normalized OTF_flip

            # reset all relevant properties based on updated attributes from other parts.
            [self.Sz, self.Sy, self.Sx] = np.shape(self.psf_ori)
            [self.Scz, self.Scy, self.Scx] = np.array([self.Sz-1, self.Sy-1, self.Sx-1] )/ 2
            [self.Soz, self.Soy, self.Sox] = np.round(np.array([self.Scz, self.Scy, self.Scx]))
            [self.FWHMz, self.FWHMy, self.FWHMx] = fwhm_PSF(self)

        def align(self, current_stack, align_size):
            # align the PSFin to align coordinates.
            [Sz2, Sy2, Sx2] = np.shape(current_stack)
            self.psf = align_size(self.psf_ori, Sx2, Sy2, Sz2)
            t=np.fft.ifftshift(self.psf)
            self.otf=np.fft.fftn(t)  # do this separately seems to be slightly faster...

    class BackwardProjector:
        def __init__(self):
            self.psf_ori = np.nan
            self.otf_ori = np.nan
            self.psf_ori_wiener = np.nan
            self.otf_ori_wiener = np.nan
            self.psf_ori_butterworth = np.nan
            self.otf_ori_butterworth = np.nan
            self.psf_ori_wiener_butterwroth = np.nan
            self.otf_ori_wiener_butterwroth = np.nan
            self.psf = np.nan
            self.otf = np.nan
            self.resx = np.nan
            self.resy = np.nan
            self.resz = np.nan
            self.px = np.nan
            self.py = np.nan
            self.pz = np.nan
            self.tx = np.nan
            self.ty = np.nan
            self.tz = np.nan
            self.beta_fpx = np.nan  # OTF cutoff frequency, in x
            self.beta_fpy = np.nan  # OTF cutoff frequency, in y
            self.beta_fpz = np.nan  # OTF cutoff frequency, in z
            self.beta_fp = np.nan   # OTF cutoff frequency, average

        def get_ready(self, fp, wbd):
            # do everything that is in preparation for producing different versions of back projectors.
            # Set resolution as PSF_fp FWHM (will worry about SIM in the future)
            self.resx = fp.FWHMx
            self.resy = fp.FWHMy
            self.resz = fp.FWHMz
            #
            # % pixel size in Fourier domain
            self.px = 1 / np.float32(fp.Sx)
            self.py = 1 / np.float32(fp.Sy)
            self.pz = 1 / np.float32(fp.Sz)
            #
            # % frequency cutoff in terms of pixels
            self.tx = 1/self.resx/self.px
            self.ty = 1/self.resy/self.py
            self.tz = 1/self.resz/self.pz
            #
            if VERBOSE:
                print(['spatial resolution cutoff:' + str(self.resx) + ' x '+str(self.resy)+' x '+str(self.resz)])
                print(['frequency resolution cutoff:' + str(self.tx) + ' x ' + str(self.ty) + ' x ' + str(self.tz)])

            self.set_cutoff_gain(fp)
            self.set_W_B_filter_param(fp, wbd)
            return

        def set_cutoff_gain(self, fp):
            # Check cutoff gains of traditional back projector
            # check cutoff gain in x:
            tplane = fp.otf_ori_flipped_abs_norm.max(axis=0)  # take maximum along z dimension, preserve y and x dimensions.
            tline = tplane.max(axis=0)  # take maximum along y dimension, preserve x dimension.
            # first edge of the frequency cutoff ring in terms of pixel index.
            to1 = np.int(np.max([np.round(fp.Scx - self.tx), 0]))
            # second edge of the frequency cutoff ring in terms of pixel index.
            to2 = np.int(np.min([np.round(fp.Scx + self.tx), fp.Sx]))
            self.beta_fpx = (tline[to1] + tline[to2])/2  # OTF frequency at the cutoff ring that intersects with x-axis
            #
            # check cutoff gain in y:
            tplane = fp.otf_ori_flipped_abs_norm.max(axis=0)  # take maximum along z dimension, preserve y and x dimensions.
            tline = tplane.max(axis=1)  # take maximum along x dimension, preserve y dimension.
            # first edge of the frequency cutoff ring in terms of pixel index.
            to1 = np.int(np.max([np.round(fp.Scy - self.ty), 0]))
            # second edge of the frequency cutoff ring in terms of pixel index.
            to2 = np.int(np.min([np.round(fp.Scy + self.ty), fp.Sy]))
            self.beta_fpy = (tline[to1] + tline[to2])/2  # OTF frequency at the cutoff ring that intersects with y-axis.
            #
            # check cutoff gain in z:
            tplane = fp.otf_ori_flipped_abs_norm.max(axis=2)  # take maximum along x dimension, preserve z and y dimensions.
            tline = tplane.max(axis=1)  # take maximum along y dimension, preserve z dimension.
            # first edge of the frequency cutoff ring in terms of pixel index.
            to1 = np.int(np.max([np.round(fp.Scz - self.tz), 0]))
            # second edge of the frequency cutoff ring in terms of pixel index.
            to2 = np.int(np.min([np.round(fp.Scz + self.tz), fp.Sz]))
            self.beta_fpz = (tline[to1] + tline[to2])/2  # OTF frequency at the cutoff ring that intersects with z-axis.
            #
            # get overall averaged OTF frequency at the cutoff.
            self.beta_fp = (self.beta_fpx + self.beta_fpy + self.beta_fpz)/3
            #
            if VERBOSE:
                print(['Cutoff gain of forward projector:' + str(self.beta_fpx) + ' x ' +  str(self.beta_fpy) +
                    ' x ' + str(self.beta_fpz) + ', Average = ' + str(beta_fp)])

            return

        def set_W_B_filter_param(self, fp, wbd):
            # wbd is the overall parent class: WBDeconv
            # set alpha value (for Wiener filter)
            if wbd.alpha == 1:
                wbd.alpha = self.beta_fp  # cutoff frequency is an attribute that belongs to BackProjector
                if VERBOSE:
                    print(['Wiener parameter adjusted as traditional BP cutoff gain: alpha = ' + str(wbd.alpha)])

            else:
                if VERBOSE:
                    print(['Wiener parameter set as input: alpha = ' + str(wbd.alpha)])

            # set beta value, for Butterworth filter
            if wbd.beta == 1:
                wbd.beta = self.beta_fp  # cutoff frequency is an attribute that belongs to BackProjector
                if VERBOSE:
                    print(['Cutoff gain adjusted as traditional BP cutoff gain: beta = ' + str(wbd.beta)])

            else:
                if VERBOSE:
                    print(['Cutoff gain set as input: beta = ' + str(wbd.beta)])

        def getTbp(self):
            # # get traditional back projector [may not need it]
            # % normalize flipped PSF: traditional back projector
            # flippedPSF = flipPSF(PSF_fp);
            # OTF_flip = fftn(ifftshift(flippedPSF));
            # OTF_abs = fftshift(abs(OTF_flip));
            # OTFmax = max(OTF_abs(:)); % find
            # maximum
            # value and position
            # M = OTFmax(1);
            # OTF_abs_norm = OTF_abs / M;
            # PSF_bp= flipPSF(PSF_fp);
            # OTF_bp = fftn(ifftshift(PSF_bp));
            # leave it for now, no need. ---- XY, 3.29.2020
            return

        def getBbp(self, fp, wbd):
            # OTF_butterworth = 1/sqrt(1+ee*(kx/kcx)^pn)
            # beta = 1/sqrt(1+ee) --> ee = 1/beta^2 - 1;
            kcx = self.tx  # width of Butterworth Filter
            kcy = self.ty  # width of Butterworth Filter
            kcz = self.tz  # width of Butterworth Filter
            ee = 1/wbd.beta**2 - 1 # epsilon square
            # create Butteworth Filter
            mask = np.zeros((fp.Sz, fp.Sy, fp.Sx), dtype=np.float32)
            for i in np.arange(0, fp.Sx):
                for j in np.arange(0, fp.Sy):
                    for k in np.arange(0, fp.Sz):
                        w = ((i-fp.Scx)/kcx)**2 + ((j-fp.Scy)/kcy)**2 + ((k-fp.Scz)/kcz)**2
                        mask[k, j, i] = 1/np.sqrt(1+ee*(w**wbd.n))  # % w^n = (kx/kcx)^pn

            self.otf_ori_butterworth = np.fft.ifftshift(mask)
            t = np.fft.ifftn(self.otf_ori_butterworth)
            t = np.real(t)
            t = np.fft.fftshift(t)
            t = t / np.sum(t.ravel())
            self.psf_ori_butterworth = t
            return

        def getWbp(self, fp, wbd):
            # % % % parameter for wiener filter;
            # OTF_flip_norm = OTF_flip/M; % Normalized OTF_flip
            # OTF_bp = OTF_flip_norm ./(abs(OTF_flip_norm).^2+alpha); % Wiener filter
            self.otf_ori_wiener = fp.otf_ori_flipped_norm / (np.abs(fp.otf_ori_flipped_norm)**2 + wbd.alpha)  # Wiener filter
            t = np.fft.ifftn(self.otf_ori_wiener)
            t = np.real(t)
            t = np.fft.fftshift(t)
            t = t / np.sum(t.ravel())
            self.psf_ori_wiener = t
            return

        def getWBbp(self, wbd, fp):
            self.getWbp(wbd, fp)
            self.getBbp(wbd, fp)
            self.otf_ori_wiener_butterwroth = self.otf_ori_butterworth * self.otf_ori_wiener
            t = np.fft.ifftn(self.otf_ori_wiener_butterwroth)
            t = np.real(t)
            t = np.fft.fftshift(t)
            t = t/np.sum(t.ravel())
            self.psf_ori_wiener_butterwroth = t
            return

        def pickbp(self, bp_type):
            if bp_type == 'Wiener-Butterworth':
                self.psf_ori = self.psf_ori_wiener_butterwroth
            elif bp_type == 'Wiener':
                self.psf_ori = self.psf_ori_wiener
            elif bp_type == 'Butterworth':
                self.psf_ori = self.psf_ori_butterworth

            return

        def align(self, current_stack, align_size):
            # align the PSFin to align coordinates.
            [Sz2, Sy2, Sx2] = np.shape(current_stack)
            self.psf = align_size(self.psf_ori, Sx2, Sy2, Sz2)
            t=np.fft.ifftshift(self.psf)
            self.otf=np.fft.fftn(t)  # do this separately seems to be slightly faster...

    def WBDeconv_1stack(self, stack):
        #------------------------------------
        #
        #   Need acceleration.
        #
        #------------------------------------
        stack[stack<self.small_value] = self.small_value
        if self.itN == 1:
            stack_estimate = stack
        else:
            stack_estimate = copy.deepcopy(stack)

        for itI in np.arange(0, self.itN):
            # stackEstimate = stackEstimate. * ConvFFT3_S(stack. / ConvFFT3_S(stackEstimate, OTF_fp), OTF_bp);
            a = self.ConvFFT3_S(stack_estimate, self.fp.otf)
            b = stack/a
            c = self.ConvFFT3_S(b, self.bp.otf)
            stack_estimate = stack_estimate*c
            stack_estimate[stack_estimate<self.small_value]=self.small_value

        self.stack_estimate = stack_estimate

    def WBDeconv_all(self):
        # ------------------------------------
        #
        #   Need to make it to deconvolve the entire time series.
        #
        #   Maybe prepare  a series of seeds... and prepare batch to submit to LC... need to think about it.
        #   deconvolution of 1 stack is ~10 minute.
        #   need a simulation stack to test for time-lapse deconvolution.
        #
        # ------------------------------------
        self.WBDeconv_1stack(self.current_stack)
        return

    def fwhm(self, x, y):
        # % Full-Width at Half-Maximum (FWHM) of the waveform y(x)
        # % The FWHM result in 'width' will be in units of 'x'
        # %
        # edited from the following source -- March 2020
        # % Rev 1.2, April 2006 (Patrick Egan)
        #
        y = y / np.max(y)
        N = y.size
        # find index of center (max or min) of pulse
        lev50 = 0.5
        if y[0] < lev50:
            centerindex = np.argmax(y)
            pol = 1
            if VERBOSE:
                print('Pulse positive')

        else:
            centerindex = np.argmin(y)
            pol = -1
            if VERBOSE:
                print('Pulse negative')

        # find first crossing.
        i = 1
        while np.sign(y[i]-lev50) == np.sign(y[i-1]-lev50):
             i += 1

        # first crossing is between y[i-1] & y[i]
        interp = (lev50 - y[i-1]) / (y[i]-y[i-1])  # calculate the interpolation point
        tlead = x[i-1] + interp*(x[i]-x[i-1])

        # find second cross point
        i = centerindex+1
        while np.sign(y[i]-lev50) == np.sign(y[i-1]-lev50) * (i <= N-1):
             i += 1

        if i != N:
            if VERBOSE:
                print('Pulse is Impulse or Rectangular with 2 edges')

            interp = (lev50 - y[i-1]) / (y[i] - y[i-1])
            ttrail = x[i-1] + interp*(x[i]-x[i-1])
            width = ttrail - tlead

        else:
            if VERBOSE:
                print('Pulse is Impulse or Rectangular with 2 edges')

            ttrail = NaN
            width = NaN

        return width

    def get_projectors(self):
        # declare a ForwardProjector object, and get it ready
        self.fp = self.ForwardProjector(self.psf_path)
        self.fp.get_ready(self.fwhm_PSF)
        # this will set the following attributes in fp: self.fp.psf_*;  self.fp.otf; self.fp.Sx/y/z,
        # self.fp.Scx/y/z, self.fp.Sox/y/z, etc.
        # declare a BackwardProjector object, and get it ready.
        self.bp = self.BackwardProjector()
        self.bp.get_ready(self.fp, self)
        self.bp.set_W_B_filter_param(self.fp, self)
        self.bp.getWBbp(self.fp, self)
        self.bp.pickbp(self.bp_type)
        # align both projectors, this will greatly expand the matrix size to match the observation 3D stack,
        # should be able to slim down. [leave for future]
        self.fp.align(self.current_stack, self.align_size)
        self.bp.align(self.current_stack, self.align_size)

        return

    def ConvFFT3_S(self, invol, otf):
        t = np.fft.fftn(invol)
        t = t * otf
        t = np.fft.ifftn(t)
        t = np.real(t)
        outvol = np.float32(t)
        return outvol

    def fwhm_PSF(self, p):
        # P is the corresponding projector object, either ForwardProjector, or BackwardProjector
        # Return back the full width at half maximun of the input PSF
        psf = p.psf_ori
        #  consider 3D input only.
        [indz, indy, indx] = np.unravel_index(np.argmax(psf, axis=None), psf.shape)

        fwhmx = self.fwhm(np.arange(0, p.Sx), psf[indz, indy, :].ravel())
        fwhmy = self.fwhm(np.arange(0, p.Sy), psf[indz, :, indx].ravel())
        fwhmz = self.fwhm(np.arange(0, p.Sz), psf[:, indy, indx].ravel())
        return [fwhmz, fwhmy, fwhmx]

    def dft_llsm(self):
        # calculate 3D discrete fourier transform from a raw llsm 3D stack without deskew.
        return

    def align_size(self, img1, Sx2, Sy2, Sz2, padValue=0):
        [Sz1, Sy1, Sx1] = np.shape(img1)
        Sx = max(Sx1, Sx2)
        Sy = max(Sy1, Sy2)
        Sz = max(Sz1, Sz2)
        imgTemp = np.ones((Sz, Sy, Sx)) * padValue

        Sox = round((Sx - Sx1) / 2)
        Soy = round((Sy - Sy1) / 2)
        Soz = round((Sz - Sz1) / 2)
        imgTemp[Soz: Soz + Sz1, Soy: Soy + Sy1, Sox: Sox + Sx1] = img1

        Sox = round((Sx - Sx2) / 2)
        Soy = round((Sy - Sy2) / 2)
        Soz = round((Sz - Sz2) / 2)
        img2 = imgTemp[Soz:Soz + Sz2, Soy: Soy + Sy2, Sox: Sox + Sx2]
        return img2

    def mygaussfit(self, x, y, h):
        # %
        # % [sigma,mu,A]=mygaussfit(x,y)
        # % [sigma,mu,A]=mygaussfit(x,y,h)
        # %
        # % this function is doing fit to the function
        # % y=A * exp( -(x-mu)^2 / (2*sigma^2) )
        # %
        # % the fitting is been done by a polyfit
        # % the lan of the data.
        # %
        # % h is the threshold which is the fraction
        # % from the maximum y height that the data
        # % is been taken from.
        # % h should be a number between 0-1.
        # % if h have not been taken it is set to be 0.2
        # % as default.
        # %
        #
        #
        # % % threshold
        # if nargin==2, h=0.2; end
        #
        # % % cutting
        # ymax=max(y);
        # xnew=[];
        # ynew=[];
        # for n=1:length(x)
        #     if y(n)>ymax*h
        #         xnew=[xnew,x(n)];
        #         ynew=[ynew,y(n)];
        #     end
        # end
        #
        # % % fitting
        # ylog=log(ynew);
        # xlog=xnew;
        # p=polyfit(xlog,ylog,2);
        # A2=p(1);
        # A1=p(2);
        # A0=p(3);
        # sigma=sqrt(-1/(2*A2));
        # mu=A1*sigma^2;
        # A=exp(A0+mu^2/(2*sigma^2));
        # return [sigma,mu,A]
        return
