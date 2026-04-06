% Copyright 2010-2014 Valerio Senni (valerio.senni@gmail.com)
% Validation-Lib is distributed under the terms
% of the GNU General Public License.
%
% This file is part of Validation-Lib.
%
% Validation-Lib is free software: you can redistribute it and/or modify
% it under the terms of the GNU General Public License as published by
% the Free Software Foundation, version 3 of the License.
%
% Validation-Lib is distributed in the hope that it will be useful,
% but WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
% GNU General Public License for more details.
%
% You should have received a copy of the GNU General Public License
% along with Validation-Lib.  If not, see <http://www.gnu.org/licenses/>.

% WARNING: The direct usage 
% PATH_TO_LIB/write_swi PATH_TO_PROGRAM/PROGRAM_NAME.pl PREDICATE_NAME SIZE OUTPUT_FILE
% does not work anymore in 2017. Moreover It is therefore revised as follows.

% usage: /usr/local/bin/swipl -q -t main -f PATH_TO_LIB/write_swi PATH_TO_LIB PATH_TO_PROGRAM/PROGRAM_NAME.pl PREDICATE_NAME SIZE OUTPUT_FILE

eval :-
   current_prolog_flag(argv,Argv),
% for debugging: write(Argv), nl,
% Bug with swipl 7.2.3
%   append(_, [Command,--,Program,Predicate,Size,OutputFile|_], Argv), 
%   file_directory_name(Command,Directory), 
% Bug fixed with
   append(_, [Directory,Program,Predicate,Size,OutputFile|_], Argv),
% for debugging: write(Directory), nl,
   string_concat(Directory,'/measure.pl',Lib),
   compile(Lib),
   compile(Program),
   input_to_number(Size,N),
   write_to_file(N,Predicate,OutputFile),
   halt.

main :-
        catch(eval, E, (print_message(error, E), fail)),
        halt.
main :-
        halt(1).
