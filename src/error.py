#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   error.py                                             :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: junruan <junruan@student.42.fr>              +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/09 08:29:49 by junruan             #+#    #+#            #
#   Updated: 2026/06/09 08:30:21 by junruan            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

"""Custom exceptions raised by the Fly-in parser and runtime."""

class ParsingError(Exception):
    """Raised when the input map file has invalid syntax."""
