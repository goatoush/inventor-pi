from time import ticks_ms, ticks_diff

class ValueFilter:

    # filters: array of filters applied sequencially, e.g. ["Median", "EMA"]
    #   SMA (Simple Moving Average) smmothes out change over time, 
    #   EMA (Exponential Moving Average) gives priority to recent values than older ones, 
    #   Median (Median Filter) removes noise and preserve sharp edges in signals
    #   Debounce (Debounce Filter) removes rapid, false signal transitions or "bounces"
    # window_size: Window size for SMA or Median filter.
    # alpha: Smoothing factor for EMA filter between 0.0 and 1.0.
    # Lower alpha = more denoising (but introduces more lag).
    # Higher alpha = faster response (but lets more noise through).
    # debounce: wait until debounce milliseconds since last value change to update value
    def __init__(self, initial_value=None, filter=None, filters=[], window_size=5, alpha=0.5, debounce=300):
        self.value = initial_value
        self.previous_value = initial_value
        self._debounced_value = None
        self._ema_value = None
        self.changed = False
        self.filters = filters
        self.debounce = debounce
        if filter is not None: self.filters = [filter]
        self.window_size = window_size
        self._sma_history = []
        self._median_history = []
        self._sorted_window = []
        self.alpha = alpha
        self.filter_map = {
            "SMA": self._sma_filter,
            "EMA": self._ema_filter,
            "Median": self._median_filter,
            "Debounce": self._debounce_filter
        }

    def _sma_filter(self, current_sample):
        self._sma_history.append(current_sample)
        if len(self._sma_history) > self.window_size: self._sma_history.pop(0) # capped at window size
        return sum(self._sma_history) / len(self._sma_history) # current average

    def _ema_filter(self, current_sample):
        if self._ema_value is None: self._ema_value = current_sample
        else:
            self._ema_value = (self.alpha * current_sample) + ((1.0 - self.alpha) * self._ema_value)
        return self._ema_value # Formula: y[n] = α * x[n] + (1 - α) * y[n-1]

    def _median_filter(self, current_sample):
        self._median_history.append(current_sample)
        self._insort_right(self._sorted_window, current_sample)
        if len(self._median_history) > self.window_size:
            oldest = self._median_history.pop(0) # capped at window size
            self._sorted_window.remove(oldest) # Remove oldest from the sorted array
        return self._sorted_window[len(self._sorted_window) // 2] # Return the middle element

    def _debounce_filter(self, current_sample):
        if self._debounced_value is None: 
            self._debounced_value = current_sample
            self._debounce_current_value = current_sample
            self._debounce_start_time = ticks_ms()
        elif self._debounce_current_value != current_sample:
            self._debounce_current_value = current_sample
            self._debounce_start_time = ticks_ms()
        elif ticks_diff(ticks_ms(), self._debounce_start_time) >= self.debounce:
            self._debounced_value = current_sample
        return self._debounced_value
        
    # Update function should be called only once during a loop, 
    # either directly or via did_change with value
    def update(self, new_value):

        # apply any smoothing filters in sequence
        for filter in self.filters: 
            if self.filter_map[filter]:
                new_value = self.filter_map[filter](new_value)

        self.changed = new_value != self.value
        if self.changed:
            self.previous_value = self.value
            self.value = new_value
        return self.value
            
    # To check if value has changed, either call update with new_value, then did_change without any value,
    # or skip the update call and call did_change with new_value, which calls update from within the function.
    # Update function should be called only once during a loop, 
    # either directly or via did_changewith value
    def did_change(self, new_value=None):
        if new_value is not None: self.update(new_value)
        return self.changed
        
    def _bisect_right(self, a, x, lo=0, hi=None):
        """Return the index where to insert item x in list a, assuming a is sorted.
        If x is already in a, the insertion point comes after the rightmost x.
        """
        if lo < 0:
            raise ValueError("lo must be non-negative")
        if hi is None:
            hi = len(a)
        while lo < hi:
            mid = (lo + hi) // 2
            if x < a[mid]:
                hi = mid
            else:
                lo = mid + 1
        return lo

    def _insort_right(self, a, x, lo=0, hi=None):
        """Insert item x in list a, and keep it sorted assuming a is sorted.
        If x is already in a, insert it to the right of the rightmost x.
        """
        pos = self._bisect_right(a, x, lo, hi)
        a.insert(pos, x)
