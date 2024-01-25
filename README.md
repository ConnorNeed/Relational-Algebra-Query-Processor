# Relational-Algebra-Query-Processor

Caution: this program uses eval function causing a significant vulnerability when used by a malicious actor. 

## Syntax

### Relation creation:
Table_Name (h1, h2, ..., hn) {

row1-1, row1-2, ..., row1-n

...

};
### Queries
* Unary operators: keyword "condition" (relation);
* binary operators: keyword "condition" (relation1)(relation2);

### Notes
* Semi-colon necessary at end of each command
* Space after keyword necessary
* Unary operators keywords: [select, project]
* Binary operators keywords: [ijoin, ljoin, rjoin, ojoin, union, minus, intersect]
* Condition must be in quotes
* queries can be linked together
* if two tables are linked that has the same column header, the second header will have the "<relation2_name>." prefixed to it
  
