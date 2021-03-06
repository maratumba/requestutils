# -*- coding: utf-8 -*-
import nose.tools as nt
from request_param import RequestParam
from request import Request
import validators as v
from mystubs import StubQueryArgs


class TestRequestFull(object):

    def get_request(self):

        rq = Request()
        RequestParam('mintime',
                     name="UTC minimum date and time",
                     description='''UTC minimum date and time
                     meaning: data are extracted if related time is greater equal to mintime
                     standard reference:  ISO 8601 (YYYY-MM-DDThh:mm:ss.ccc)''',
                     validators=[v.ValidatorDateTimeRange('1970-01-01T00:00:00.000', 'now')]
                     ).addTo(rq)

        RequestParam('maxtime',
                     name="UTC maximum date and time",
                     description='''UTC maximum date and time
                     meaning: data are extracted if related time is less or equal to maxtime
                     standard reference:  ISO 8601 (YYYY-MM-DDThh:mm:ss.ccc)''',
                     validators=[v.ValidatorDateTimeRange('1970-01-01T00:00:00.000', 'now')]
                     ).addTo(rq)

        # ensure mintime is smaller than maxtime
        rq.addPostValidator(v.ValidatorPostSmaller('mintime', 'maxtime'))

        #
        # Geographic region parameters
        #

        RequestParam('minlat',
                     name='Minimum latitude of the selection area',
                     description='''earthquakes and stations to calculate Vp/Vs are extracted if latitude is greater or equal to minlat
                     standard reference:  ISO 6709''',
                     validators=[v.ValidatorNumberRange(-90, 90)]
                     ).addTo(rq)

        RequestParam('maxlat',
                     name='Maximum latitude of the selection area',
                     description='''earthquakes and stations to calculate Vp/Vs are extracted if latitude is less or equal to maxlat
                     standard reference:  ISO 6709''',
                     validators=[v.ValidatorNumberRange(-90, 90)]
                     ).addTo(rq)

        rq.addPostValidator(v.ValidatorPostSmaller('minlat', 'maxlat'))

        RequestParam('minlon',
                     name='Minimum longitude of the selection area',
                     description='''earthquakes and stations to calculate Vp/Vs are extracted if longitude is greater or equal to minlon
                     standard reference:  ISO 6709''',
                     validators=[v.ValidatorNumberRange(-180, 180)]
                     ).addTo(rq)

        RequestParam('maxlon',
                     name='Maximum longitude of the selection area',
                     description='''earthquakes and stations to calculate Vp/Vs are extracted if longitude is less or equal to maxlon
                     standard reference:  ISO 6709''',
                     validators=[v.ValidatorNumberRange(-180, 180)]
                     ).addTo(rq)

        rq.addPostValidator(v.ValidatorPostSmaller('minlon', 'maxlon'))

        #
        # SPECIFIC PARAMS:
        # these parameters may are not mandatory but in this case they are set to NFO specifically chosen presets
        #

        # Earthquakes

        RequestParam('mineqdep',
                     name='Minimum depth of earthquakes',
                     description='''earthquakes to calculate Vp/Vs are extracted if depth is greater or equal to mineqdep
                     standard reference:  ISO 6709 negative a.s.l. positive b.s.l.''',
                     unit='km',
                     validators=[v.ValidatorNumberRange(-6378, -9.00)]
                     ).addTo(rq)

        RequestParam('maxeqdep',
                     name='Maximum depth of earthquakes',
                     description='''earthquakes to calculate Vp/Vs are extracted if depth is less or equal to mineqdep
                     standard reference:  ISO 6709 negative a.s.l. positive b.s.l.''',
                     unit='km',
                     validators=[v.ValidatorNumberRange(-6378, -9.0)]
                     ).addTo(rq)

        rq.addPostValidator(v.ValidatorPostSmaller('mineqdep', 'maxeqdep'))

        RequestParam('minnp',
                     name='Minimum number of P waves',
                     description='''number of p-waves onset observations
                     meaning: minimum number of p-waves onset observations, with quality hypoinverse standard weight less equal to maxpw, that one earthquake has to have to be extracted
                     standard reference: integer, no standard''',
                     default=1,
                     validators=[v.ValidatorInt(), v.ValidatorNumberMin(0)]
                     ).addTo(rq)

        RequestParam('minns',
                     name='Minimum number of S waves',
                     description='''number of s-waves onset observations
                     meaning: minimum number of s-waves onset observations, with quality hypoinverse standard weight less equal to maxsw, that one earthquake has to have to be extracted
                     standard reference: integer, no standard''',
                     default=1,
                     validators=[v.ValidatorInt(), v.ValidatorNumberMin(0)]
                     ).addTo(rq)

        RequestParam('maxpw',
                     name='quality hypoinverse standard weight',
                     description='''quality hypoinverse standard weight
                     meaning: maximum quality weight allowed for a p-wave reading so that it is counted for earthquake selection
                     standard reference: integer, hypoinverse 2000 standard (0 high quality, 3 worse, 4 not used)''',
                     validators=[v.ValidatorInt(), v.ValidatorNumberRange(0, 4)]
                     ).addTo(rq)

        RequestParam('maxsw',
                     name='quality hypoinverse standard weight',
                     description='''mum quality weight allowed for a s-wave reading so that it is counted for earthquake selection
                     standard reference: integer, hypoinverse 2000 standard (0 high quality, 3 worse, 4 not used)''',
                     validators=[v.ValidatorInt(), v.ValidatorNumberRange(0, 4)]
                     ).addTo(rq)

        RequestParam('minps',
                     name='number of P and S couples per earthquake',
                     description='''minimum number of p- and s-waves observed at one single station, with quality hypoinverse
                     standard weight less equal to maxpw and maxsw respectively, that one earthquake has to have to be extracted''',
                     validators=[v.ValidatorInt(), v.ValidatorNumberMin(0)]
                     ).addTo(rq)

        RequestParam('maxgap',
                     name='degrees of azimuthal stations distribution gap per earthquake',
                     description='''maximum allowed azimuthal gap so that a earthquakes is selected;
                     this parameters tends to guarantee a more feasible location and to exclude earthquakes
                     at the edge of the network coverage''',
                     validators=[v.ValidatorNumberRange(0, 360)]
                     ).addTo(rq)

        RequestParam('midi',
                     name='horizontal distance of the closest station from a earthquake',
                     description='''maximum distance of the closest station from an earthquake so that it
                     can be extracted, this parameters tends to guarantee a more feasible depth''',
                     unit='km',
                     default=40000,
                     validators=[v.ValidatorNumberRange(0, 40000)]
                     ).addTo(rq)

        RequestParam('maxherr',
                     name='maximum allowed formal horizontal error in earthquake location',
                     description='''the mean formal horizontal error directly given by
                     the location code or calculated as sqrt(errX²+errY*2) or from the uncertainty 2D or 3D ellipsoid parameters  (see the specific location code reference manual)''',
                     default=40000,
                     unit='km',
                     validators=[v.ValidatorNumberRange(0, 40000)]
                     ).addTo(rq)

        RequestParam('maxverr',
                     name='maximum allowed formal vertical error in earthquake location',
                     description='''is the mean formal vertical error directly given by the location code or calculated from the uncertainty 3D ellipsoid
                     parameters (see the specific location code reference manual)''',
                     default=6378,
                     unit='km',
                     validators=[v.ValidatorNumberRange(0, 6378)]
                     ).addTo(rq)

        return rq

    def no_test_pass(self):
        '''
        test request with all parameters
        '''
        userparams = StubQueryArgs(dict(
            mintime='2001-01-01T00:00:00.000',
            maxtime='2000-01-01T00:00:00.000',
            minlat=30,          # -90, 90 and smaller than maxlat
            maxlat=50,          # -90, 90
            minlon=40,          # -180, 180 and smaller than maxlon
            maxlon=60,          # -180, 180
            mineqdep=-70,       # -6378, -9 and smaller than maxeqdep
            maxeqdep=-30,       # -6378, -9
            minnp=2,            # number of p waves, int, min: 0
            minns=3,            # number of s waves, int, min: 0
            maxpw=3,            # int, 0, 4
            maxsw=3,            # int, 0, 4
            minps=4,            # 0, +
            maxgap=150,         # azim gap 0, 360
            midi=70,            # horiz dist of closest sta
            maxherr=300,        # 0, 4000
            maxverr=200         # 0, 6378
        ))

        rq = self.get_request()
        rq.bind(userparams)
        rq.validate()
        # nt.eq_(rq.is_valid, False)
        nt.eq_(rq.errors, [])
        nt.eq_(rq.global_errors[0].message, '<mintime> should be smaller than <maxtime>')
