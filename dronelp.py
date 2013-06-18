#!/usr/bin/env python

"""
Creates a 'score' for a drone to fly based on the image contours,
prints it to stdout.
"""

from optparse import OptionParser
from skimage import data, measure, io
from matplotlib import pyplot
import numpy
import csv


# Constants - defaults.
DEFAULT_OPTS = {
    'approxX': 10,
    'approxY': 10,
    'cotourLevel': 0.8,
    'pointsNum': 200
    }

MESSAGES = {
    'fileNotFound': {
        'type': 'error',
        'message': 'File not found'
        },
    'fileNotSpecified': {
        'type': 'error',
        'message': 'Please, specify the file!'
        },
    'contoursExported': {
        'type': 'ok',
        'message': 'points exported to file'
        }
    }

class Message():
    def __init__(self, code=None):
        self.code = code

    def get_message(self, code):
        try:
            return MESSAGES[code]
        except:
            try:
                return MESSAGES[self.code]
            except:
                pass

class ImageContours():
    def __init__(self, img=None):
        self.img = img
        try:
            self.imgfile = io.imread(self.img, as_grey=True)
        except:
            self.imgfile = None
        self.msg = Message()
        self.contours = None
        self.z_scale = 1

    def build_contours(self, **kwargs):
        """
        Build contours with given options.
        **kwargs are:
        approxX - Approximate X value (1..20), default 10;
        approxY - Approximate Y value (1..20), default 10;
        cotourLevel - Contour level (0.1..1.0), default 0.8;
        pointsNum - Minimum number of points in the contour, default 200.
        """
        if self.imgfile is None:
            return self.msg.get_message('fileNotSpecified')

        self.approxX = float(kwargs.get('approxX', DEFAULT_OPTS['approxX']))
        self.approxY = float(kwargs.get('approxY', DEFAULT_OPTS['approxY']))
        self.pointsNum = int(kwargs.get('pointsNum', DEFAULT_OPTS['pointsNum']))
        self.cotourLevel = float(kwargs.get('cotourLevel',
                                            DEFAULT_OPTS['cotourLevel']))

        # Construct data.
        x, y = self.approxX, self.approxY

        # Find contours at a given level.
        contours = measure.find_contours(self.imgfile, self.cotourLevel)

        # Filling Z.
        # Unroll contours to get max and min values.
        contours_that_count = [c for c in contours if len(c) >= self.pointsNum]
        unrolled = []
        for c in contours_that_count[0]:
            unrolled += c.tolist()
        lo, hi = int(numpy.floor(min(unrolled))), int(numpy.ceil(max(unrolled)))
        z_distrib = numpy.random.uniform(lo, hi, len(contours_that_count))
        z_distrib = z_distrib.astype(numpy.int64).tolist()
        z_distrib.sort()

        # Save z_scale for future scaling (take successive numbers
        # from disptrib, because hi - lo gives too big scale factor).
        self.z_scale = z_distrib[1] - z_distrib[0]

        # The more dots in a contour, the closer it to the ground.
        contours_len = sorted([len(c) for c in contours_that_count])
        contours_len.reverse()

        # Create array for new contours.
        new = numpy.zeros((1, 3), dtype=int)

        for n, contour in enumerate(contours_that_count):
            cont = contour.astype(numpy.int64)
            curr = numpy.zeros((1, 2), dtype=int)[0]
            try:
                valZ = z_distrib[contours_len.index(len(contour))]
            except:
                valZ = 0
            # Approximate contours ("First order approx").
            for point in cont:
                if numpy.any(numpy.greater(numpy.abs(curr - point), [x, y])):
                    # Add a point to contour, inject Z value
                    new = numpy.append(new,
                                       [[point[0], point[1], int(valZ)]],
                                       axis=0)
                    # Update current point for comparisson.
                    curr = point

        # Remove first row [0, 0]
        new = new[1:]

        # Update self.contours.
        self.contours = new

        return self.contours

    def plot_contours(self, **kwargs):
        """
        Plots image and its contours obtained with given options.
        """
        if self.imgfile is None:
            return self.msg.get_message('fileNotSpecified')

        pyplot.imshow(self.imgfile, interpolation='bicubic')
        pyplot.plot(self.contours[:, 1], self.contours[:, 0], linewidth=2)
        pyplot.axis('image')
        pyplot.xticks([])
        pyplot.yticks([])
        pyplot.show()

    def export_csv(self, **kwargs):
        """
        Exports coordinates to CSV file
        (to the same dir, where image file is stored).
        """
        if self.contours is None:
            self.build_contours()

        delimiter = kwargs.get('delimiter', ',')
        quotechar = kwargs.get('quotechar', '"')

        # Create CSV file.
        curr_dir, fname = self.img.rsplit('/', 1)
        csvname = fname.split('.')[0] + '.csv'
        csvfile = open('/'.join([curr_dir, csvname]), 'wb')
        csvwriter = csv.writer(csvfile,
                               delimiter=delimiter,
                               quotechar=quotechar,
                               quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['x', 'y', 'z'])

        for n, contour in enumerate(self.contours):
            csvwriter.writerow(contour)

        return '%s %s %s' % (n,
                             self.msg.get_message('contoursExported')['message'],
                             csvname)

    def build_instructions(self, **kwargs):
        """
        Creates instructions for flying drone
        amnd saves it to the `score` list of dicts.
        """
        if self.contours is None:
            self.build_contours()

        # Initial instructions.
        score = [
            (1, 'action', 'takeoff'), # Take off.
            (3, 'speed', 0.3), # Give it 2sec to stabilize, increase speed.
            (3.10000, 'action', 'move_up'),
            (4.0000, 'action', 'hover')
            ]

        time_scale = self.approxX + self.approxY
        timemark = 4.0

        contours = self.contours.copy()
        contours = contours.tolist()
        vec_curr = numpy.asarray(contours.pop(0))
        while len(contours) > 0:
            vec_next = numpy.asarray(contours.pop(0))

            xc, yc, zc = vec_curr
            x, y, z = vec_next
            _x = x - xc
            _y = y - yc
            _z = z - zc

            # Height change (with scaling depending on z scale).
            if _z != 0:
                if _z > 0:
                    action = 'move_up'
                elif _z < 0:
                    action = 'move_down'
                score.append(tuple((timemark, 'action', 'hover')))
                timemark += 0.8
                score.append(tuple((timemark, 'action', action)))
                timemark += (_z / self.z_scale)
                score.append(tuple((timemark, 'action', 'hover')))
                timemark += 0.8

            # Direction change.
            # Applying "second order approximation" here:
            # ignore if the change is too small.
            turn = min(abs(_x), abs(_y))
            if turn <= 10:
                continue
            if turn == abs(_x):
                action = 'turn_left'
            else:
                action = 'turn_right'
            score.append(tuple((timemark, 'action', action)))
            timemark += (turn / time_scale)

            # Fly forward.
            fly = numpy.absolute(numpy.linalg.norm(vec_next - vec_curr))
            score.append(tuple((timemark, 'action', 'move_forward')))
            timemark += (fly / time_scale)

            vec_curr = vec_next.copy()

        # Final instructions.
        score.append(tuple((timemark + 1, 'action', 'hover')))
        score.append(tuple((timemark + 2, 'action', 'land')))

        for act in score:
            print "\t(%.5f, '%s', '%s')," % act

        return score


def main(opts, args):
    if args:
        filename = args[0].strip()
    else:
        print "Please, specify filename (should be JPG file)."
        return

    try:
        kwargs = dict((k, getattr(opts, k)) for k in DEFAULT_OPTS.keys())
    except:
        return Message().get_message('fileNotSpecified')

    img = ImageContours(filename)
    contours = img.build_contours(**kwargs)
    score = img.build_instructions()

    # Export contours to CSV file.
    if opts.csv:
        print img.export_csv()

    # Plot obtained contours.
    if opts.plot:
        img.plot_contours()

    print 'Done'

if __name__ == '__main__':
    # Process command line options, start the process, report on the results.
    cmdparser = OptionParser(usage="usage: python %prog [Options] image.jpg")
    cmdparser.add_option('-l', '--level',
                         action='store', dest='cotourLevel',
                         default=DEFAULT_OPTS.get('cotourLevel', 0.8),
                         help= 'Contour level (0.1..1.0), default %s' %\
        DEFAULT_OPTS.get('cotourLevel', 0.8))
    cmdparser.add_option('-x', '--approxx',
                         action='store', dest='approxX',
                         default=DEFAULT_OPTS.get('approxX', 10),
                         help='Approximate X value (1..20), default %s' %\
        DEFAULT_OPTS.get('approxX', 10))
    cmdparser.add_option('-y', '--approxy',
                         action='store', dest='approxY',
                         default=DEFAULT_OPTS.get('approxY', 10),
                         help='Approximate Y value (1..20), default %s' %\
        DEFAULT_OPTS.get('approxY', 10))
    cmdparser.add_option('-p', '--points',
                         action='store', dest='pointsNum',
                         default=DEFAULT_OPTS.get('pointsNum', 200),
                         help= 'Minimum number of points in the contour, default %s' %\
        DEFAULT_OPTS.get('pointsNum', 200))
    cmdparser.add_option('-c', '--csv',
                         action='store_true', dest='csv', default=False,
                         help= 'Export to CSV file')
    cmdparser.add_option('-t', '--plot',
                         action='store_true', dest='plot', default=False,
                         help= 'Plot contours')

    opts, args = cmdparser.parse_args()
    main(opts, args)
